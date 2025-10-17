# Icarus

Icarus is a multiprotocol honeypot designed to attract and identify malicious actors. It listens on various TCP and UDP ports, collects information about attackers, and reports them to AbuseIPDB.

## Features

*   **Multiprotocol Honeypot:** Listens on a wide range of TCP and UDP ports to mimic vulnerable services.
*   **Dynamic Port Configuration:** Easily configure which ports to listen on through the `icarus.config` file.
*   **AbuseIPDB Reporting:** Automatically reports the IP addresses of attackers to AbuseIPDB.
*   **Threat Feed:** Can feed collected data to a "Largfeed" server to build a custom threat feed.
*   **Easy Configuration:** A simple configuration file (`icarus.config`) allows for easy customization.
*   **Docker Support:** Includes a `Dockerfile` for easy containerized deployment.

## Installation

### Docker (Recommended)

1.  Clone the repository:
    ```bash
    git clone https://github.com/tbiens/icarus.git
    ```
2.  Navigate to the `icarus` directory:
    ```bash
    cd icarus
    ```
3.  Create and edit the configuration file:
    ```bash
    nano icarus.config
    ```
    *   See the [Configuration](#configuration) section for more details on the available options.
4.  Build and run the Docker container:
    ```bash
    sudo bash start.sh
    ```

### Manual Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/tbiens/icarus.git
    ```
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Create and edit the configuration file:
    ```bash
    cp icarus.config.example icarus.config
    nano icarus.config
    ```
    *   See the [Configuration](#configuration) section for more details on the available options.
4.  Run the application:
    ```bash
    python3 icarus.py
    ```

## Configuration

The `icarus.config` file is used to configure the application.

| Section      | Option         | Description                                                                                                                               |
| ------------ | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `[IPDBAPI]`  | `AbuseIPDB`    | Enable or disable AbuseIPDB reporting (`yes` or `no`).                                                                                    |
| `[IPDBAPI]`  | `IPDBAPI`      | Your AbuseIPDB API key.                                                                                                                   |
| `[SYSLOG]`   | `Syslog`       | Enable or disable syslog logging (`yes` or `no`).                                                                                         |
| `[SYSLOG]`   | `IP`           | The IP address of your syslog server.                                                                                                     |
| `[SYSLOG]`   | `PORT`         | The port of your syslog server.                                                                                                           |
| `[LARGFEED]` | `Largfeed`     | Enable or disable the Largfeed integration (`yes` or `no`).                                                                               |
| `[LARGFEED]` | `Server`       | The address of your Largfeed server.                                                                                                      |
| `[LARGFEED]` | `Port`         | The port of your Largfeed server.                                                                                                         |
| `[HTTPPOST]` | `Httppost`     | Enable or disable the HTTP POST integration (`yes` or `no`).                                                                              |
| `[HTTPPOST]` | `url`          | The URL to which to POST the data.                                                                                                        |
| `[PORTS]`    | `tcpports`     | A comma-separated list of TCP ports to listen on.                                                                                         |
| `[PORTS]`    | `udpports`     | A comma-separated list of UDP ports to listen on.                                                                                         |


## Usage

Once the application is running, it will listen on the configured ports and log any activity to the console and to the `logs` directory.

## Integrations

### AbuseIPDB

Icarus can report the IP addresses of attackers to AbuseIPDB. To enable this feature, you need to set `AbuseIPDB = yes` in the `[IPDBAPI]` section of the `icarus.config` file and provide your AbuseIPDB API key.

### Largfeed

Icarus can feed collected data to a "Largfeed" server to build a custom threat feed. Largfeed is a separate project that is not included with Icarus.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the GPL License. See the `LICENSE` file for more details.