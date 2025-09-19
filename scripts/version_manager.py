#!/usr/bin/env python3
"""
Automatic version management script for Serbian Transport integration.
Updates version in manifest.json, JavaScript files, and creates git tags.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple
from datetime import datetime

class VersionManager:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.manifest_path = self.project_root / "custom_components/serbian_transport/manifest.json"
        self.js_card_path = self.project_root / "custom_components/serbian_transport/www/transport-card.js"
        
    def get_current_version(self) -> str:
        """Get current version from manifest.json"""
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
        return manifest['version']
    
    def get_latest_git_tag(self) -> str:
        """Get latest git tag"""
        try:
            result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], 
                                  capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "v0.0.0"
    
    def parse_commits_since_tag(self, tag: str) -> List[Tuple[str, str]]:
        """Parse commits since last tag and categorize them"""
        try:
            result = subprocess.run(['git', 'log', f'{tag}..HEAD', '--oneline'], 
                                  capture_output=True, text=True, check=True)
            commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
        except subprocess.CalledProcessError:
            result = subprocess.run(['git', 'log', '--oneline'], 
                                  capture_output=True, text=True, check=True)
            commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        categorized = []
        for commit in commits:
            if not commit:
                continue
            
            # Parse conventional commit format
            message = commit.split(' ', 1)[1] if ' ' in commit else commit
            
            if message.startswith(('feat:', 'feature:')):
                categorized.append(('minor', message))
            elif message.startswith(('fix:', 'bugfix:')):
                categorized.append(('patch', message))
            elif message.startswith(('BREAKING:', 'breaking:')):
                categorized.append(('major', message))
            elif any(message.lower().startswith(prefix) for prefix in [
                'add', 'enhance', 'improve', 'implement', 'refactor'
            ]):
                categorized.append(('minor', message))
            else:
                categorized.append(('patch', message))
        
        return categorized
    
    def increment_version(self, current_version: str, increment_type: str) -> str:
        """Increment version based on type"""
        # Remove 'v' prefix if present
        version = current_version.lstrip('v')
        
        try:
            major, minor, patch = map(int, version.split('.'))
        except ValueError:
            print(f"Warning: Could not parse version {version}, defaulting to 2.0.0")
            major, minor, patch = 2, 0, 0
        
        if increment_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif increment_type == 'minor':
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        return f"{major}.{minor}.{patch}"
    
    def update_manifest_version(self, new_version: str):
        """Update version in manifest.json"""
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
        
        manifest['version'] = new_version
        
        with open(self.manifest_path, 'w') as f:
            json.dump(manifest, f, indent=4)
        
        print(f"✅ Updated manifest.json version to {new_version}")
    
    def update_js_version(self, new_version: str):
        """Update version in JavaScript file"""
        if not self.js_card_path.exists():
            print(f"⚠️  JavaScript file not found: {self.js_card_path}")
            return
        
        with open(self.js_card_path, 'r') as f:
            content = f.read()
        
        # Update version in comment
        pattern = r'// Transport Card v[\d.]+.*'
        replacement = f'// Transport Card v{new_version} - {datetime.now().strftime("%Y-%m-%d")}'
        content = re.sub(pattern, replacement, content)
        
        with open(self.js_card_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated JavaScript version to v{new_version}")
    
    def create_changelog(self, commits: List[Tuple[str, str]], new_version: str):
        """Create or update CHANGELOG.md"""
        changelog_path = self.project_root / "CHANGELOG.md"
        
        # Create changelog entry
        changelog_entry = f"""
## [v{new_version}] - {datetime.now().strftime("%Y-%m-%d")}

"""
        
        # Categorize changes
        features = [msg for type_, msg in commits if type_ == 'minor']
        fixes = [msg for type_, msg in commits if type_ == 'patch']
        breaking = [msg for type_, msg in commits if type_ == 'major']
        
        if features:
            changelog_entry += "### ✨ Features\n"
            for feature in features:
                changelog_entry += f"- {feature}\n"
            changelog_entry += "\n"
        
        if fixes:
            changelog_entry += "### 🐛 Bug Fixes\n"
            for fix in fixes:
                changelog_entry += f"- {fix}\n"
            changelog_entry += "\n"
        
        if breaking:
            changelog_entry += "### ⚠️ BREAKING CHANGES\n"
            for change in breaking:
                changelog_entry += f"- {change}\n"
            changelog_entry += "\n"
        
        # Read existing changelog or create new
        if changelog_path.exists():
            with open(changelog_path, 'r') as f:
                existing_content = f.read()
            
            # Insert new entry after header
            if "# Changelog" in existing_content:
                header, rest = existing_content.split("# Changelog", 1)
                content = f"# Changelog{changelog_entry}{rest}"
            else:
                content = f"# Changelog{changelog_entry}\n{existing_content}"
        else:
            content = f"# Changelog{changelog_entry}"
        
        with open(changelog_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated CHANGELOG.md with v{new_version}")
    
    def create_git_tag(self, version: str, commits: List[Tuple[str, str]]):
        """Create git tag with release notes"""
        tag_name = f"v{version}"
        
        # Create tag message
        tag_message = f"Release {tag_name}\n\n"
        if commits:
            tag_message += "Changes:\n"
            for _, msg in commits[:10]:  # Limit to 10 commits
                tag_message += f"- {msg}\n"
        
        try:
            subprocess.run(['git', 'tag', '-a', tag_name, '-m', tag_message], check=True)
            print(f"✅ Created git tag {tag_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create git tag: {e}")
            return False
    
    def get_all_tags(self) -> List[str]:
        """Get all git tags sorted by version"""
        try:
            result = subprocess.run(['git', 'tag', '-l'], capture_output=True, text=True, check=True)
            tags = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            # Sort tags by version
            def version_key(tag):
                # Remove 'v' prefix and split by dots
                version = tag.lstrip('v')
                try:
                    return tuple(map(int, version.split('.')))
                except ValueError:
                    return (0, 0, 0)
            
            return sorted(tags, key=version_key)
        except subprocess.CalledProcessError:
            return []
    
    def get_tag_date(self, tag: str) -> str:
        """Get creation date of a git tag"""
        try:
            result = subprocess.run(['git', 'log', '-1', '--format=%ai', tag], 
                                  capture_output=True, text=True, check=True)
            date_str = result.stdout.strip()
            # Parse and reformat date
            date_obj = datetime.strptime(date_str[:10], '%Y-%m-%d')
            return date_obj.strftime('%Y-%m-%d')
        except (subprocess.CalledProcessError, ValueError):
            return datetime.now().strftime('%Y-%m-%d')
    
    def parse_commits_between_tags(self, from_tag: str, to_tag: str) -> List[Tuple[str, str]]:
        """Parse commits between two tags"""
        try:
            if from_tag:
                range_spec = f'{from_tag}..{to_tag}'
            else:
                # First tag - get all commits up to it
                range_spec = to_tag
            
            result = subprocess.run(['git', 'log', range_spec, '--oneline'], 
                                  capture_output=True, text=True, check=True)
            commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
        except subprocess.CalledProcessError:
            return []
        
        categorized = []
        for commit in commits:
            if not commit:
                continue
            
            # Parse conventional commit format
            message = commit.split(' ', 1)[1] if ' ' in commit else commit
            
            if message.startswith(('feat:', 'feature:')):
                categorized.append(('minor', message))
            elif message.startswith(('fix:', 'bugfix:')):
                categorized.append(('patch', message))
            elif message.startswith(('BREAKING:', 'breaking:')):
                categorized.append(('major', message))
            elif any(message.lower().startswith(prefix) for prefix in [
                'add', 'enhance', 'improve', 'implement', 'refactor'
            ]):
                categorized.append(('minor', message))
            else:
                categorized.append(('patch', message))
        
        return categorized
    
    def create_full_changelog(self):
        """Create complete CHANGELOG.md for all existing tags"""
        tags = self.get_all_tags()
        
        if not tags:
            print("❌ No git tags found")
            return
        
        print(f"📋 Found {len(tags)} tags: {', '.join(tags)}")
        
        changelog_content = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n"
        
        # Process tags in reverse order (newest first)
        for i, tag in enumerate(reversed(tags)):
            prev_tag = tags[len(tags) - i - 2] if i < len(tags) - 1 else None
            
            print(f"📝 Processing {tag}...")
            
            # Get commits for this tag
            commits = self.parse_commits_between_tags(prev_tag, tag)
            tag_date = self.get_tag_date(tag)
            
            # Create changelog entry
            changelog_content += f"## [{tag}] - {tag_date}\n\n"
            
            if commits:
                # Categorize changes
                features = [msg for type_, msg in commits if type_ == 'minor']
                fixes = [msg for type_, msg in commits if type_ == 'patch']
                breaking = [msg for type_, msg in commits if type_ == 'major']
                
                if breaking:
                    changelog_content += "### ⚠️ BREAKING CHANGES\n"
                    for change in breaking:
                        changelog_content += f"- {change}\n"
                    changelog_content += "\n"
                
                if features:
                    changelog_content += "### ✨ Features\n"
                    for feature in features:
                        changelog_content += f"- {feature}\n"
                    changelog_content += "\n"
                
                if fixes:
                    changelog_content += "### 🐛 Bug Fixes\n"
                    for fix in fixes:
                        changelog_content += f"- {fix}\n"
                    changelog_content += "\n"
                
                # Add other changes
                other_changes = [msg for type_, msg in commits if type_ not in ['minor', 'patch', 'major']]
                if other_changes:
                    changelog_content += "### 🔧 Other Changes\n"
                    for change in other_changes:
                        changelog_content += f"- {change}\n"
                    changelog_content += "\n"
            else:
                changelog_content += "- Initial release or no commit details available\n\n"
        
        # Write changelog
        changelog_path = self.project_root / "CHANGELOG.md"
        with open(changelog_path, 'w') as f:
            f.write(changelog_content)
        
        print(f"✅ Created complete CHANGELOG.md with {len(tags)} releases")
        print(f"📄 File: {changelog_path}")
    
    def analyze_history(self):
        """Analyze complete git history and show statistics"""
        tags = self.get_all_tags()
        current_version = self.get_current_version()
        
        print("📊 SERBIAN TRANSPORT - VERSION HISTORY ANALYSIS")
        print("=" * 50)
        print(f"📋 Current version: {current_version}")
        print(f"🏷️  Total tags: {len(tags)}")
        
        if tags:
            print(f"📅 First release: {tags[0]} ({self.get_tag_date(tags[0])})")
            print(f"📅 Latest tag: {tags[-1]} ({self.get_tag_date(tags[-1])})")
            print()
            
            total_commits = 0
            total_features = 0
            total_fixes = 0
            total_breaking = 0
            
            print("📋 RELEASE HISTORY:")
            print("-" * 30)
            
            for i, tag in enumerate(reversed(tags)):
                prev_tag = tags[len(tags) - i - 2] if i < len(tags) - 1 else None
                commits = self.parse_commits_between_tags(prev_tag, tag)
                
                features = len([msg for type_, msg in commits if type_ == 'minor'])
                fixes = len([msg for type_, msg in commits if type_ == 'patch'])
                breaking = len([msg for type_, msg in commits if type_ == 'major'])
                
                total_commits += len(commits)
                total_features += features
                total_fixes += fixes
                total_breaking += breaking
                
                tag_date = self.get_tag_date(tag)
                print(f"{tag:12} ({tag_date}) - {len(commits):2} commits | "
                      f"✨{features:2} features | 🐛{fixes:2} fixes | ⚠️{breaking:2} breaking")
            
            print("-" * 30)
            print(f"📊 TOTALS: {total_commits} commits | "
                  f"✨{total_features} features | 🐛{total_fixes} fixes | ⚠️{total_breaking} breaking")
        
        # Check unreleased commits
        if tags:
            unreleased = self.parse_commits_since_tag(tags[-1])
            if unreleased:
                print(f"\n🚧 UNRELEASED: {len(unreleased)} commits since {tags[-1]}")
                for type_, msg in unreleased[:5]:
                    print(f"   - {msg}")
                if len(unreleased) > 5:
                    print(f"   ... and {len(unreleased) - 5} more")
        
        print()
    
    def determine_version_increment(self, commits: List[Tuple[str, str]]) -> str:
        """Determine version increment type based on commits"""
        has_major = any(msg.startswith(('BREAKING', 'breaking')) for _, msg in commits)
        has_minor = any(msg.startswith(('feat', 'feature', 'add', 'enhance', 'improve', 'implement')) for _, msg in commits)
        has_patch = any(msg.startswith(('fix', 'bugfix')) for _, msg in commits)
        
        if has_major:
            return 'major'
        elif has_minor:
            return 'minor'
        elif has_patch:
            return 'patch'
        else:
            return None
    
    def increment_version(self, current_version: str, bump_type: str) -> str:
        """Increment version based on type"""
        major, minor, patch = map(int, current_version.split('.'))
        
        if bump_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif bump_type == 'minor':
            minor += 1
            patch = 0
        elif bump_type == 'patch':
            patch += 1
        
        return f"{major}.{minor}.{patch}"
    
    def bump_version(self, force_type: str = None) -> str:
        """Main function to bump version"""
        current_version = self.get_current_version()
        latest_tag = self.get_latest_git_tag()
        
        print(f"📋 Current version: {current_version}")
        print(f"📋 Latest git tag: {latest_tag}")
        
        # Get commits since last tag
        commits = self.parse_commits_since_tag(latest_tag)
        
        if not commits and not force_type:
            print("🔄 No new commits found. No version bump needed.")
            return current_version
        
        print(f"📝 Found {len(commits)} commits since {latest_tag}")
        
        # Determine increment type
        if force_type:
            increment_type = force_type
        else:
            increment_type = 'patch'  # default
            for commit_type, _ in commits:
                if commit_type == 'major':
                    increment_type = 'major'
                    break
                elif commit_type == 'minor' and increment_type != 'major':
                    increment_type = 'minor'
        
        # Calculate new version
        new_version = self.increment_version(current_version, increment_type)
        
        print(f"🚀 Bumping version: {current_version} → {new_version} ({increment_type})")
        
        # Update files
        self.update_manifest_version(new_version)
        self.update_js_version(new_version)
        self.create_changelog(commits, new_version)
        
        return new_version

def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage versions for Serbian Transport integration')
    parser.add_argument('action', choices=['bump', 'tag', 'show', 'history', 'changelog'], 
                       help='Action to perform')
    parser.add_argument('--type', choices=['major', 'minor', 'patch'], 
                       help='Force version increment type')
    parser.add_argument('--create-tag', action='store_true', 
                       help='Create git tag after version bump')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what new version would be without making changes')
    parser.add_argument('--version-only', action='store_true', 
                       help='For show command: output only version number')
    
    args = parser.parse_args()
    
    vm = VersionManager()
    
    if args.action == 'show':
        current = vm.get_current_version()
        latest_tag = vm.get_latest_git_tag()
        if args.version_only:
            print(current)
        else:
            print(f"Current version: {current}")
            print(f"Latest git tag: {latest_tag}")
    
    elif args.action == 'bump':
        if args.dry_run:
            # Just show what the new version would be
            current_version = vm.get_current_version()
            latest_tag = vm.get_latest_git_tag()
            commits = vm.parse_commits_since_tag(latest_tag)
            
            if commits:
                bump_type = vm.determine_version_increment(commits)
                if args.type:
                    bump_type = args.type
                
                if bump_type:
                    new_version = vm.increment_version(current_version, bump_type)
                    print(new_version)  # Just output the version for scripts
                else:
                    print(current_version)  # No changes needed
            else:
                print(current_version)  # No commits since last tag
        else:
            new_version = vm.bump_version(args.type)
            
            if args.create_tag:
                latest_tag = vm.get_latest_git_tag()
                commits = vm.parse_commits_since_tag(latest_tag)
                vm.create_git_tag(new_version, commits)
    
    elif args.action == 'tag':
        current = vm.get_current_version()
        latest_tag = vm.get_latest_git_tag()
        commits = vm.parse_commits_since_tag(latest_tag)
        vm.create_git_tag(current, commits)
    
    elif args.action == 'history':
        vm.analyze_history()
    
    elif args.action == 'changelog':
        vm.create_full_changelog()

if __name__ == "__main__":
    main()
