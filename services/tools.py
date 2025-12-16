#!/usr/bin/env python3
import sqlite3
from typing import Optional

from langchain_core.tools import tool

DATABASE_NAME: str = './resources/mail-providers.db'


# https://python.langchain.com/docs/how_to/custom_tools/
@tool(parse_docstring=True)
def get_mail_providers() -> list[str]:
    """
    Retrieves a list of mail provider names from the database.

    Returns:
        list[str]: A list of mail provider names.  Returns an empty list on error.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Select the 'name' column from the 'mail_providers' table
        cursor.execute("SELECT name FROM mail_providers")
        rows = cursor.fetchall()

        # Extract the provider names from the result rows
        providers = [row[0] for row in rows]  # Assuming name is the first column
        return providers

    except sqlite3.Error as e:
        print(f"Error retrieving mail providers: {e}")
        return []  # Return an empty list in case of an error

    finally:
        if conn:
            conn.close()

@tool(parse_docstring=True)
def get_mail_provider_configuration(provider_name: str) -> Optional[str]:
    """
    Retrieves the configuration for a specific mail provider from the database
    and formats it into a string.

    Args:
        provider_name (str): The name of the mail provider.

    Returns:
        Optional[str]: A formatted string containing the mail provider configuration,
                       or None if the provider is not found or an error occurs.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Select the configuration details for the given provider name.
        cursor.execute(
            """
            SELECT imap_server, smtp_server, socket_type, socket_type_smtp, auth_method_smtp
            FROM mail_providers
            WHERE name = ?
            """,
            (provider_name,),  # Use a tuple to pass the parameter
        )
        row = cursor.fetchone()  # Fetch only one row

        if row:
            imap_server, smtp_server, socket_type, socket_type_smtp, auth_method_smtp = row
            # Format the output string.
            config_string = (
                f"imap_server: {imap_server}\n"
                f"smtp_server: {smtp_server}\n"
                f"socket_type: {socket_type}\n"
                f"socket_type_smtp: {socket_type_smtp}\n"
                f"auth_method_smtp: {auth_method_smtp}"
            )
            return config_string
        else:
            print(f"Mail provider '{provider_name}' not found in the database.")
            return None  # Return None if the provider is not found

    except sqlite3.Error as e:
        print(f"Error retrieving mail provider configuration: {e}")
        return None  # Return None in case of an error

    finally:
        if conn:
            conn.close()