# Changelog
## [v2.2.0] - 2025-09-19

### ✨ Features
- Refactor release workflow: improve changelog extraction using sed for better accuracy, add logging for fallback scenarios, and enhance handling of recent commits when no changelog content is found.


## [v2.1.0] - 2025-09-19

### ✨ Features
- Enhance Serbian Transport integration: add station selection feature with dropdown interface in Transport Card, improve error handling in data fetching, and update card styling for better user experience.
- Refactor Serbian Transport integration: streamline API request handling, simplify city determination logic, and enhance error management in data fetching.
- Enhance README for Serbian Transport integration: add one-click installation instructions, improve visibility of HACS integration links, and update feature descriptions for better clarity.
- Refactor Serbian Transport integration: implement migration for config entries, enhance error handling in API requests, and improve frontend card UI with new features and styling adjustments.
- Enhance Transport Card: adjust styling for stop ID display and improve code formatting
- Refactor hacs.json: remove unnecessary render_changelog property
- Refactor Transport Card: improve code formatting and enhance JSON configuration
- Refactor Transport Card: improve arrival times display format and enhance stop item structure
- Refactor Transport Card: improve layout and styling for stop and arrival times
- Refactor Transport Card: enhance arrival times rendering and improve layout for arrivals list
- Refactor Transport Card: enhance styling and improve stop rendering logic
- Refactor Serbian Transport integration: update import path for add_extra_js_url from frontend module
- Refactor Serbian Transport integration: replace async_register_resource with add_extra_js_url for JS module registration
- Refactor Serbian Transport integration: streamline static path registration and Lovelace resource registration
- Refactor Serbian Transport integration: update Lovelace resource registration to use the correct import path
- Refactor Serbian Transport integration: register Lovelace resource for improved accessibility
- Refactor Serbian Transport integration: create necessary directories and copy component files for static path registration
- Refactor Serbian Transport integration: update static path registration to use 'path' for improved clarity
- Refactor Serbian Transport integration: update static path registration for improved clarity and organization
- Refactor Serbian Transport integration: update static path registration to use new syntax for improved clarity
- Refactor Serbian Transport integration: replace static path registration with async_register_static_paths for improved efficiency
- Refactor Serbian Transport integration: enhance error handling for coordinates and ensure unique ID configuration
- Refactor Serbian Transport integration: replace async_register_resource with manual resource registration and improve logging
- Refactor Serbian Transport integration: update static path registration to use new resource path and improve error handling
- Refactor Serbian Transport integration: replace static_path_from_config with register_static_path and clean up unused code
- Refactor Serbian Transport integration: update static path registration to use static_path_from_config method
- Refactor Serbian Transport integration: update static path registration method, enhance error handling, and improve config flow imports
- Refactor Serbian Transport config flow: enhance user input handling, add options flow, and update documentation
- Enhance Serbian Transport integration: update static path registration, improve config entry setup, and add dependencies for frontend and http
- feat: commit message

### 🐛 Bug Fixes
- Update README for Serbian Transport integration: change version badge to 2.0.0, add new features including intelligent station selection and automated releases, enhance screenshots and configuration details, and improve clarity in the features section.
- Revamp README for Serbian Transport integration: expand features section, enhance installation instructions, and improve configuration options for better user experience.
- Update Transport Card to v2.2.0: simplify design with new animations, progress bars for arrival times, and enhanced visual UI configuration.
- Remove HACS Card Action workflow file
- Update Serbian Transport integration: add icon and refine .gitignore entries
- Update README: add attribution for bus icon from Flaticon
- Update README: add Serbian transport integration details and installation instructions
- Update README: add supported cities for Serbian public transport integration
- Update README and refactor Transport Card layout for improved styling and structure
- Remove deprecated files and configurations; introduce new HACS card workflow for Serbian Transport integration
- Full rework



All notable changes to this project will be documented in this file.

## [v0.1.16] - 2025-02-05

### ✨ Features
- Refactor dashboard component to enhance performance and error handling; update API URL configuration and improve panel registration logic

### 🐛 Bug Fixes
- Bump version to 0.1.16

## [v0.1.15] - 2025-02-05

### ✨ Features
- Refactor CityDashboardPanel registration to improve custom element definition and panel registration logic

### 🐛 Bug Fixes
- Bump version to 0.1.15

## [v0.1.14] - 2025-02-05

### ✨ Features
- Refactor CityDashboardPanel registration to ensure it waits for 'home-assistant' definition before registering the panel

### 🐛 Bug Fixes
- Bump version to 0.1.14
- Merge branch 'main' of https://github.com/dzarlax/HASS-Serbian-transport

## [v0.1.13] - 2025-02-05

### ✨ Features
- Refactor Beograd Transport component: remove unused files and update dashboard module to use new entry point

### 🐛 Bug Fixes
- Bump version to 0.1.13

## [v0.1.12] - 2025-02-05

### 🐛 Bug Fixes
- Bump version to 0.1.12
- Update Beograd Transport component to change dashboard module URL and output filename

## [v0.1.11] - 2025-02-05

### ✨ Features
- Refactor Beograd Transport component to use DOMAIN for frontend URL and update dashboard registration

### 🐛 Bug Fixes
- Bump version to 0.1.11

## [v0.1.10] - 2025-02-05

### ✨ Features
- Enhance file copying logic to include assets directory for Serbian Transport component setup

### 🐛 Bug Fixes
- Bump version to 0.1.10
- Merge branch 'main' of https://github.com/dzarlax/HASS-Serbian-transport

## [v0.1.9] - 2025-02-05

### ✨ Features
- Refactor file copying logic to create directories in www/community for Serbian Transport component setup

### 🐛 Bug Fixes
- Bump version to 0.1.9

## [v0.1.8] - 2025-02-05

### ✨ Features
- Implement file copying for Serbian Transport component setup

### 🐛 Bug Fixes
- Bump version to 0.1.8
- Merge branch 'main' of https://github.com/dzarlax/HASS-Serbian-transport
- Bump version to 0.1.7
- Merge branch 'main' of https://github.com/dzarlax/HASS-Serbian-transport
- Rename integration from Beograd Transport to Serbian Transport

## [v0.1.7] - 2025-02-05

### 🐛 Bug Fixes
- Bump version to 0.1.7
- Merge branch 'main' of https://github.com/dzarlax/HASS-Serbian-transport
- Update config flow documentation for Serbian Transport integration

## [v0.1.6] - 2025-02-05

### ✨ Features
- Add domain entry for Beograd Transport in hacs.json

### 🐛 Bug Fixes
- Bump version to 0.1.6

## [v0.1.5] - 2025-02-05

### 🐛 Bug Fixes
- Bump version to 0.1.5
- Update integration references from City Dashboard to Beograd Transport in configuration and service worker files

## [v0.1.4] - 2025-02-05

### ✨ Features
- Refactor City Dashboard integration to Beograd Transport, updating constants, translations, and manifest files; remove old City Dashboard files.

### 🐛 Bug Fixes
- Bump version to 0.1.4
- Update HACS workflow for Beograd Transport integration, modifying paths and versioning in manifest files
- Merge branch 'main' of https://github.com/dzarlax/HASS-Serbian-transport
- Rename City Dashboard to Serbian Transport and update related files

## [v0.1.3] - 2025-02-05

### 🐛 Bug Fixes
- Bump version to 0.1.3
- Rename zip file and update component name to Serbian Transport

## [v0.1.2] - 2025-02-05

### 🐛 Bug Fixes
- Bump version to 0.1.2
- Rename City Dashboard to Belgrade Transport and update related configurations
- first commit

