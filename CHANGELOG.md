# Changelog

All notable changes to the CraxCore Location Tracker will be documented in this file.

## [1.0.0] - 2025-05-19

### Added

-   Initial release of CraxCore Location Tracker
-   Support for all Bangladeshi mobile operators
-   Password protection with secure hashing
-   BTS tower info simulation for location tracking
-   Geocoding for address lookup
-   Tracking history with encryption
-   System capability checker
-   Integration with OpenCellID API
-   Export functionality for tracking data
-   Interactive map visualization

### Security

-   Added salt-based password hashing system
-   Created secure password manager module
-   Added setup_security.py for enhanced security features
-   Improved API key handling with environment variables
-   Updated .gitignore to exclude sensitive files
-   Configured secure file permissions

### Changed

-   Updated default password from "password" to "CraxCoreLocat"
-   Improved error handling and user feedback
-   Enhanced user interface with rich formatting
-   Updated installation process with virtual environment support
-   Created wrapper scripts for easier usage

### Fixed

-   Fixed duplicate code in display_about() function
-   Fixed password manager import issues
-   Fixed incorrect string concatenation
-   Fixed syntax errors in main.py
-   Improved error handling for missing dependencies

## [0.9.0] - 2025-05-15

### Added

-   Beta version with basic tracking functionality
-   Simple password protection
-   Support for major Bangladeshi operators
-   Basic location simulation

### Known Issues

-   No encryption for tracking history
-   Limited error handling
-   Basic security implementation
