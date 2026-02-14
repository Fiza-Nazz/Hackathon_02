"""
Test script to verify MCP tools are working properly.
"""

def test_all_tools():
    print("Testing all MCP tools...")
    print("="*50)

    # Test add_task
    print("\n1. Testing add_task tool:")
    from backend.mcp_server.tools.add_task import add_task

    result = add_task(
        user_id="test_user_123",
        title="Test task from script",
        description="This is a test task created via script"
    )

    print(f"Add task result: {result}")

    if result["success"]:
        task_id = result["data"]["task_id"]
        print(f"Task created successfully with ID: {task_id}")

        # Test list_tasks
        print("\n2. Testing list_tasks tool:")
        from backend.mcp_server.tools.list_tasks import list_tasks

        result = list_tasks(user_id="test_user_123", status="all")
        print(f"List tasks result: {result}")

        # Test complete_task
        print("\n3. Testing complete_task tool:")
        from backend.mcp_server.tools.complete_task import complete_task

        result = complete_task(user_id="test_user_123", task_id=task_id)
        print(f"Complete task result: {result}")

        # Test list_tasks again to see updated status
        print("\n4. Testing list_tasks after completion:")
        result = list_tasks(user_id="test_user_123", status="completed")
        print(f"Completed tasks result: {result}")

        # Test update_task
        print("\n5. Testing update_task tool:")
        from backend.mcp_server.tools.update_task import update_task

        result = update_task(
            user_id="test_user_123",
            task_id=task_id,
            title="Updated test task"
        )
        print(f"Update task result: {result}")

        # Test delete_task
        print("\n6. Testing delete_task tool:")
        from backend.mcp_server.tools.delete_task import delete_task

        result = delete_task(user_id="test_user_123", task_id=task_id)
        print(f"Delete task result: {result}")

    else:
        print("Failed to create task")

    print("\n" + "="*50)
    print("All tests completed!")

if __name__ == "__main__":
    test_all_tools()