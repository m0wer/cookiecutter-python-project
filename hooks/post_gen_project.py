"""Configuration tasks to be run after the template has been generated."""

import os
import subprocess  # nosec
import sys
from base64 import b64encode
from typing import Any, Dict, Optional, Tuple

import requests
import sh
from cryptography.hazmat.backends import (
    default_backend as crypto_default_backend,
)
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from nacl import encoding, public


def encrypt_secret(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(
        public_key.encode("utf-8"), encoding.Base64Encoder()
    )
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))

    return b64encode(encrypted).decode("utf-8")


def get(
    url: str,
    token: str,
    method: str = "get",
    data: Optional[Dict[str, Any]] = None,
) -> requests.models.Response:
    """Handle errors and configuration in requests queries."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    if method == "post":
        response = requests.post(url, headers=headers, json=data)
    elif method == "put":
        response = requests.put(url, headers=headers, json=data)
    else:
        response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response


def initialize_git_repository() -> None:
    """Prepare the git repository."""
    print("    * Initializing the project git repository")

    try:
        sh.git.init()
        sh.git.branch("-m", "master", "main")
        sh.git.remote(
            "add",
            "origin",
            "git@github.com:{{ cookiecutter.github_user }}/"
            "{{ cookiecutter.project_slug }}.git",
        )
        sh.git.add(".")
        sh.git.commit("-m", "feat: create initial project structure")
        sh.git.checkout("-b", "gh-pages")
        sh.git.checkout("-b", "feat/initial_iteration")

        print("    * Pushing initial changes to main")
        sh.git.push("--force", "--set-upstream", "origin", "main")
        sh.git.push("--force", "--set-upstream", "origin", "gh-pages")
        sh.git.push(
            "--force", "--set-upstream", "origin", "feat/initial_iteration"
        )
        sh.git.push("--force")
    except sh.ErrorReturnCode as error:
        print("There was an error creating the Git repository.")
        print(str(error.stderr, "utf8"))
        sys.exit(1)


def format_code() -> None:
    """Correct source code following the Black style."""
    print("    * Make repository Black linter compliant.")
    sh.black("setup.py", "src", "docs/examples", "tests")


def initialize_requirement_files() -> None:
    """Generate the python dependencies requirement files."""
    print("    * Generate requirements.txt")
    sh.pip_compile()
    print("        * Generate docs/requirements.txt")
    sh.pip_compile(
        "docs/requirements.in",
    )
    print("        * Generate requirements-dev.txt")
    sh.pip_compile("requirements-dev.in")


def get_password(password_command: str) -> str:
    """Get password from pass passwordstore."""
    try:
        password: str = (
            subprocess.check_output(password_command, shell=True)  # nosec
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError as error:
        print(error.output)

    return password


def generate_ssh_key() -> Tuple[str, str]:
    """Generate public and private ssh keys."""
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=4096,
    )

    private_key = str(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ),
        "utf8",
    )

    public_key = str(
        key.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH,
        )
        + b" {{ cookiecutter.author_email }}",
        "utf8",
    )

    return private_key, public_key


def configure_github_repository() -> None:
    """Configure the github repository."""
    github_url = "https://api.github.com"
    print("* Configure the Github repository")
    github_token = get_password("{{ cookiecutter.github_token_pass_command }}")

    print("    * Check if the repository exists")
    try:
        get(
            url=(
                f"{github_url}/repos/{{ cookiecutter.github_user }}/"
                "{{ cookiecutter.project_slug }}"
            ),
            token=github_token,
        )
        repository_exists = True
    except requests.exceptions.HTTPError:
        repository_exists = False

    if not repository_exists:
        print("    * Creating Github repository")
        try:
            get(
                url=f"{github_url}/user/repos",
                method="post",
                data={
                    "name": "{{ cookiecutter.project_slug }}",
                    "description": "{{ cookiecutter.project_description }}",
                    "homepage": (
                        "https://{{ cookiecutter.github_user }}.github.io/"
                        "{{ cookiecutter.project_slug }}"
                    ),
                },
                token=github_token,
            )
        except requests.exceptions.HTTPError:
            print("Error creating the repository in github")
            sys.exit(1)

    print("* Check if the repository is initialized")
    try:
        repo_commits = get(
            url=(
                f"{github_url}/repos/{{ cookiecutter.github_user }}/"
                "{{ cookiecutter.project_slug }}/commits"
            ),
            token=github_token,
        ).json()
        if len(repo_commits) < 1:
            initialize_requirement_files()
            format_code()
            initialize_git_repository()
    except requests.exceptions.HTTPError:
        initialize_requirement_files()
        format_code()
        initialize_git_repository()


def main() -> None:
    """Run the post hooks."""
    print(
        """
#########################
# Post generation hooks #
#########################
"""
    )

    configure_github_repository()


if __name__ == "__main__" and os.environ.get("COOKIECUTTER_TESTING") != "true":
    main()
