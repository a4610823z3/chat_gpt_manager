var getAllUsers;
var currentPage = 1;
var authorization = document.getElementById("authorization");
$(document).ready(function () {
  const addUserForm = document.getElementById("add-user-form");

  const userTable = document.getElementById("user-table");

  getAllUsers = function getAllUsers(pageIndex) {
    var pageSize = document.getElementById("pageSize").value;
    if (pageSize == "") {
      pageSize = 10;
    }
    axios
      .get("/users?page_index=" + pageIndex + "&page_size=" + pageSize, {
        headers: get_header(),
      })
      .then((response) => {
        const message_error = response.data.error;
        if (message_error != "" && message_error != undefined) {
          alert(message_error);
          return;
        }
        userTable.innerHTML = "";
        response.data.forEach((user) => {
          const row = `
                        <tr data-id="${user.id}" >
                            <td data-field="id">${user.id}</td>
                            <td data-field="name">${user.name}</td>
                            <td data-field="key">${user.key}</td>
                            <td>
                            <button type="button" class="btn btn-danger delete-user-btn" data-toggle="modal" onclick="deleteUser('${user.id}')">Delete</button>
                            </td>
                        </tr>`;
          userTable.insertAdjacentHTML("beforeend", row);
          $(".edit-user-btn").click(function (e) {
            e.preventDefault();

            // 将用户信息填充到表单中
            var id = $(this).closest("tr").find("td:first-child").text();
            var name = $(this).closest("tr").find("td:nth-child(2)").text();
            var key = $(this).closest("tr").find("td:nth-child(3)").text();
            $("#edit-user-id").val(id);
            $("#edit-user-name").val(name);
            $("#edit-user-key").val(key);

            // 显示模态框
            $("#edit-user-modal").modal("show");
          });

          $("#edit-user-modal").on("hidden.bs.modal", function () {
            // 关闭模态框时清空表单内容
            $("#edit-user-form")[0].reset();
          });
        });
      })
      .catch((error) => console.log(error));
  };

  function loadPaginator() {
    let paginator = $(".pagination");
    paginator.empty(); // 清空分页器

    // 添加“上一页”按钮
    paginator.append(`<a class="button is-primary" onclick="pre()">上一页</a>`);
    paginator.append(`<input id="currentPageIndex" value='1' size=2 type="text" class="field"></input>`);
    // 添加“下一页”按钮
    paginator.append(
      `<a class="button is-primary" onclick="next()">下一页</a>`
    );
    paginator.append(
      `显示条数:<input id="pageSize" value='10' size=2 type="number" class="field"></input>`
    );
  }
  loadPaginator();

  addUserForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(addUserForm);
    const userData = Object.fromEntries(formData.entries());
    axios
      .post("/users", userData, {
        headers: get_header(),
      })
      .then((response) => {
        var message_error = response.data.error;
        if (message_error != "" && message_error != undefined) {
          alert(message_error);
          return;
        } else {
          alert("User added successfully");
        }
        getAllUsers(currentPage);
        // 添加隐藏模态框时的清空表单内容事件
        $("#add-user-form")[0].reset();
        $("#add-user-modal").modal("hide");
      });
  });
});

function deleteUser(userId) {
  if (confirm("Are you sure you want to delete this user?")) {
    axios
      .delete(`/users/${userId}`, {
        headers: get_header(),
      })
      .then((response) => {
        const message_error = response.data.error;
        if (message_error != "" && message_error != undefined) {
          alert(message_error);
          return;
        } else {
          alert("User deleted successfully");
        }
        getAllUsers(currentPage);
      })
      .catch((error) => console.log(error));
  }
}

function pre() {
  currentPage = currentPage - 1;
  if (currentPage < 0) {
    currentPage = 1;
  }
  getAllUsers(currentPage);
  var currentPageInput = document.getElementById("currentPageIndex")
  currentPageInput.value = currentPage;
}

function next() {
  if (currentPage < 0) {
    currentPage = 1;
  }
  currentPage = currentPage + 1;
  getAllUsers(currentPage);
  var currentPageInput = document.getElementById("currentPageIndex")
  currentPageInput.value = currentPage;
}

function get_header() {
  return { Authorization: authorization.value };
}
function setAuthorization() {
  getAllUsers(currentPage);
}
