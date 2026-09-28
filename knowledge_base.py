knowledge_base = [

    {
        "id": "KB001",
        "title": "VPN Troubleshooting Guide",
        "category": "Network Connectivity",
        "content": """
        Step-by-step instructions for resolving VPN connection issues.

        1. Verify that the user has an active internet connection.
        2. Check VPN client configuration.
        3. Verify the VPN server address.
        4. Verify authentication settings.
        5. Restart the VPN service.
        6. Clear cached credentials if authentication fails.
        """
    },

    {
        "id": "KB002",
        "title": "Network Firewall Configuration",
        "category": "IT Policies",
        "content": """
        Corporate firewalls must allow VPN traffic.

        Verify that VPN traffic is permitted on the required ports,
        including ports 500 and 4500 for IPsec-based VPN connections.
        """
    },

    {
        "id": "KB003",
        "title": "VPN Authentication Problems",
        "category": "Authentication",
        "content": """
        If VPN authentication fails, verify the username, password,
        MFA configuration, cached credentials, and authentication
        method configured in the VPN client.
        """
    }
]


if __name__ == "__main__":

    print("Knowledge Base Loaded Successfully!")
    print("Total Documents:", len(knowledge_base))

    for document in knowledge_base:
        print(
            document["id"],
            "-",
            document["title"]
        )