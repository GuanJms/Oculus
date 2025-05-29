# Oculus Trading & Backtesting Framework

## Overview
Oculus is a modular, extensible framework for quantitative trading, backtesting, and research. It features a robust hub/session architecture, strategy abstraction, and pluggable adapters for execution, data, and time systems. The framework is designed for both research and production, supporting live trading, paper trading, and backtesting with a focus on flexibility and scalability. Oculus is built with a focus on performance, maintainability, and ease of use, making it ideal for both beginners and advanced users in quantitative finance.

## Features
- **Hub/Session Architecture**: Centralized management of trading, backtesting, and simulation sessions. This architecture allows for easy orchestration of multiple strategies and sessions, providing a unified interface for managing trading operations.
- **Strategy Abstraction**: Define custom trading strategies using the `StrategyRule` base class. This abstraction allows for easy implementation of new strategies and integration with the existing framework.
- **Adapters**: Pluggable execution, data, and time system adapters for easy integration and extension. These adapters allow for seamless integration with various data sources, execution venues, and time systems.
- **User Interface**: Dash-based UI for monitoring and interaction (see `user_interfaces/dash_app`). The UI provides real-time monitoring of trading sessions, strategy performance, and system status.
- **Comprehensive Testing**: Includes a suite of tests and test data for robust development. The testing framework ensures that all components of the system are functioning as expected.
- **Extensible & Modular**: Easily add new strategies, adapters, and modules. The modular design allows for easy extension and customization of the framework.

## Directory Structure
```
Oculus/
├── calculators/           # Financial and statistical calculators
├── data_process_module/   # Data processing and transaction management
├── data_system/           # Data system, adapters, and domain managers
├── execution_module/      # Execution session and portfolio management
├── execution_system/      # Execution adapters, order management, and signal generation
├── initialization_module/ # Initialization logic and configuration
├── integration_hub/       # Hub/session management and orchestration
├── starter_brainstorm/    # Notebooks and brainstorming
├── status_module/         # Status tracking and reporting
├── strategics/            # Strategy logic and rule definitions
├── test_data/             # Test datasets
├── Tests/                 # Test scripts and configs
├── user_interfaces/       # User interfaces (e.g., Dash app)
├── utils/                 # Utility functions and helpers
└── session.py             # Core session abstraction
```

## Installation
- **Python Version**: Python 3.8+
- **Dependencies**: This project does not currently include a `requirements.txt`. Please create one based on your environment and the modules you use. Typical dependencies may include `pandas`, `numpy`, `dash`, and others relevant to trading and data processing.

```bash
# Example (create your own requirements.txt):
pip install pandas numpy dash
```

## Quick Start
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Oculus
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt  # (if you have created one)
   ```
3. **Run a backtest or live session:**
   - Define your strategy by subclassing `StrategyRule` (see `strategics/repo/core/strategy/strategy_rule.py`).
   - Use the integration hub to configure and run sessions (see `integration_hub/`).
   - For UI, see `user_interfaces/dash_app/`. The Dash app provides a user-friendly interface for monitoring and interacting with your trading sessions.

## Usage
- **Defining Strategies:**
  - Inherit from `StrategyRule` and implement the `execute` method. This method should define the logic for your trading strategy, including signal generation and order execution.
- **Running Backtests:**
  - Use `BacktestHub` in `integration_hub` to configure and run backtests with your strategy and parameters. The backtest hub provides a unified interface for managing backtest sessions.
- **Adapters:**
  - Plug in or extend execution, data, and time system adapters as needed. These adapters allow for seamless integration with various data sources, execution venues, and time systems.
- **Sessions:**
  - Manage multiple sessions and strategies concurrently using the hub/session architecture. This allows for easy orchestration of multiple trading sessions and strategies.

## API Documentation
- **Hub**: The central component for managing trading sessions and strategies. It provides methods for configuring and running sessions, as well as managing adapters.
- **Session**: The core abstraction for trading sessions. It provides methods for managing session status and lifecycle.
- **StrategyRule**: The base class for defining trading strategies. It provides methods for executing strategies and managing strategy parameters.
- **Adapters**: Pluggable components for integrating with various data sources, execution venues, and time systems. They provide a unified interface for interacting with external systems.

## Architecture & Design
Oculus is built on a modular, layered architecture designed for flexibility, scalability, and maintainability. The framework follows these key design principles:

- **Modularity**: Each component (e.g., data system, execution system, integration hub) is designed as a separate module, allowing for easy extension and replacement.
- **Abstraction**: Core abstractions like `Session`, `Hub`, and `StrategyRule` provide a unified interface for managing trading operations, making it easy to implement new strategies and adapters.
- **Pluggable Adapters**: The framework uses adapters to integrate with external systems (e.g., data sources, execution venues, time systems), allowing for seamless integration and extension.
- **Hub/Session Architecture**: The hub/session architecture provides a centralized way to manage trading sessions and strategies, allowing for easy orchestration and monitoring.
- **Separation of Concerns**: Each module is responsible for a specific aspect of the trading process, ensuring that the system is maintainable and testable.

This architecture allows Oculus to be used for a wide range of trading and backtesting scenarios, from simple strategies to complex, multi-asset trading systems.

## Testing
- Test scripts are located in the `Tests/` directory and within module-specific `tests/` folders. These tests ensure that all components of the system are functioning as expected.
- Run tests using your preferred test runner, e.g.:
  ```bash
  python -m unittest discover Tests
  ```

## Contributing
Contributions are welcome! Please:
- Follow best practices for Python development.
- Write clear, concise commit messages.
- Add or update tests for new features or bug fixes.
- Open issues or pull requests for discussion.
