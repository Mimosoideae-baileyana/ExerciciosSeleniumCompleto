import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os


@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # roda sem interface
    driver = webdriver.Chrome(options=chrome_options)
    caminho_html = os.path.abspath("index.html")
    driver.get(f"file://{caminho_html}")
    yield driver
    driver.quit()


# ----------------- LOGIN ------------------
def test_login_sucesso(driver):
    driver.find_element(By.ID, "username").send_keys("admin")
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys("1234")
    time.sleep(1)
    driver.find_element(By.ID, "loginBtn").click()
    time.sleep(1)
    message = driver.find_element(By.ID, "message").text
    time.sleep(1)
    assert message == "Login bem-sucedido! 2"


def test_login_falha(driver):
    driver.find_element(By.ID, "username").send_keys("usuario")
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys("senhaerrada")
    time.sleep(1)
    driver.find_element(By.ID, "loginBtn").click()
    time.sleep(1)
    message = driver.find_element(By.ID, "message").text
    time.sleep(1)
    assert message == "Usuário ou senha incorretos."


# ----------------- CHECKBOXES -----------------
def test_checkboxes(driver):
    cb1 = driver.find_element(By.ID, "cb1")
    cb2 = driver.find_element(By.ID, "cb2")
    cb3 = driver.find_element(By.ID, "cb3")

    # Selecionar todos
    cb1.click()
    time.sleep(1)
    cb2.click()
    time.sleep(1)
    cb3.click()
    time.sleep(1)
    assert cb1.is_selected()
    assert cb2.is_selected()
    assert cb3.is_selected()

    # Desmarcar o cb2
    cb2.click()
    time.sleep(1)
    assert not cb2.is_selected()


# ----------------- RADIO BUTTONS -----------------
def test_radiobuttons(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    radios = driver.find_elements(By.NAME, "gender")

    # Selecionar Masculino
    for r in radios:
        if r.get_attribute("value") == "Masculino":
            r.click()
            time.sleep(1)
    assert any(r.is_selected() and r.get_attribute(
        "value") == "Masculino" for r in radios)

    # Selecionar Outro
    for r in radios:
        if r.get_attribute("value") == "Outro":
            r.click()
            time.sleep(1)
    assert any(r.is_selected() and r.get_attribute(
        "value") == "Outro" for r in radios)


# ----------------- DROPDOWN -----------------
def test_dropdown(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    select = Select(driver.find_element(By.ID, "country"))
    time.sleep(1)
    select.select_by_visible_text("Brasil")
    time.sleep(1)
    assert select.first_selected_option.text == "Brasil"

    select.select_by_visible_text("EUA")
    time.sleep(1)
    assert select.first_selected_option.text == "EUA"


# ----------------- LISTA DE TAREFAS -----------------
def test_lista_tarefas(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    input_task = driver.find_element(By.ID, "taskInput")
    add_btn = driver.find_element(By.ID, "addTaskBtn")
    task_list = driver.find_element(By.ID, "taskList")

    # Adicionar 3 tarefas
    tarefas = ["Tarefa 1", "Tarefa 2", "Tarefa 3"]
    for t in tarefas:
        input_task.send_keys(t)
        time.sleep(1)
        add_btn.click()
        time.sleep(1)

    items = task_list.find_elements(By.TAG_NAME, "li")
    time.sleep(1)
    assert len(items) == 3

    # Remover a segunda tarefa
    items[1].find_element(By.CLASS_NAME, "remove-btn").click()
    time.sleep(1)
    items = task_list.find_elements(By.TAG_NAME, "li")
    assert len(items) == 2
    assert "Tarefa 2" not in [i.text for i in items]

    # Tentar adicionar tarefa vazia
    time.sleep(1)
    add_btn.click()
    message = driver.find_element(By.ID, "taskMessage").text
    time.sleep(1)
    assert message == "Digite uma tarefa!"
