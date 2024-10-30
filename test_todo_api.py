import requests, uuid

ENDPOINT = "https://todo.pixegami.io"

# response = requests.get(ENDPOINT)
# print(response)

# data = response.json()
# print(data)

# status_code = response.status_code
# print(status_code)

def test_can_call_endpoint():
    # Act
    response = requests.get(ENDPOINT)
    # Assert
    assert response.status_code == 200

def test_can_create_task():
    # Arrange
    payload = new_task_payload()

    # Act
    create_task_response = create_task(payload)

    # Assert
    assert create_task_response.status_code == 200

    # Arrange
    data = create_task_response.json()
    # print(data)
    task_id = data["task"]["task_id"]
    # print(task_id)

    # Act
    get_task_response = get_task(task_id)

    # Assert
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]
    assert get_task_data["is_done"] == payload["is_done"]

def test_can_update_task():
    # Arrange
    payload = new_task_payload()
    create_task_response  = create_task(payload=payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]
 
    # Act
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "my updated content",
        "is_done": True
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

def test_can_list_tasks():
    # Arrange
    number_of_tasks = 3
    user_id = f"test_user_{uuid.uuid4().hex}"
    for _ in range(number_of_tasks):
        payload = new_task_payload(user_id)
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    # Act
    list_tasks_response = list_tasks(user_id)

    # Assert
    assert list_tasks_response.status_code == 200
    tasks = list_tasks_response.json()["tasks"]
    assert len(tasks) == number_of_tasks

def test_can_delete_task():
    # Arrange
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # Act
    delete_task_response = delete_task(task_id)

    # Assert
    assert delete_task_response.status_code == 200
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404

def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def update_task(new_payload):
    return requests.put(ENDPOINT + "/update-task", json=new_payload)

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")

def new_task_payload(user_id=None):
    content = f"test_content_{uuid.uuid4().hex}"
    if user_id == None:
        user_id = f"test_user_{uuid.uuid4().hex}"

    # print(f"Creating task for user {user_id} with content {content}")

    return {
        "content": content,
        "user_id": user_id,
        "is_done": False
    }