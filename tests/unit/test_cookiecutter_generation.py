def test_bake_project(cookies):
    result = cookies.bake(
        extra_context={
            "project_name": "helloworld",
            "github_token_pass_command": "echo testpassword",
        }
    )

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "helloworld"
    assert result.project_path.is_dir()
