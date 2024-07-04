//搜索功能
// 定义一个搜索函数
function search() {
    // 获取当前页面的URL
    var pageUrl = window.location.href;
    // 获取用户输入的数据
    var keyword = $("#search-input").val();
    // 判断用户输入是否为空
    if (keyword) {
        // 使用 jQuery 的 ajax 方法向后端发送请求
        $.ajax({
            url: "/search/", // 后端地址
            type: "POST", // 请求方式
            data: { // 请求参数
                keyword: keyword, // 用户输入的数据
                pageUrl: pageUrl
            },
            dataType: "JSON", // 响应数据类型
            success: function (data) { // 请求成功的回调函数
                if (data.redirect) {
                    window.location.href = data.redirect + '?arg=' + data.arg;  // 如果后端返回了重定向URL和参数，那么在前端进行重定向并传递参数
                }
            },
            error: function (error) { // 请求失败的回调函数
                // 处理错误信息，例如提示用户
                console.log(error);
            }
        });
    } else {
        // 提示用户输入不能为空
        alert("请输入搜索内容");
    }
}

// 页面加载完成后执行该函数
document.addEventListener('DOMContentLoaded', function () {
    //回车也可以触发搜索功能
    $(document).ready(function () {
        // 当用户在输入框中按下回车键时，触发search函数
        $("#search-input").keypress(function (event) {
            if (event.which == 13) {  // 13是回车键的键码
                search();  // 调用search函数
            }
        });
    });

    // 定义一个函数，用于在向导航栏添加和删除“responsive”响应类之间切换
    function toggleNavbar() {
        // 获取导航栏的元素
        var navbar = document.getElementById("myNavbar");
        // 如果导航栏没有响应类，就添加响应类
        if (navbar.className === "navbar") {
            navbar.className += " responsive";
        } else {
            // 否则，就移除响应类
            navbar.className = "navbar";
        }
    }

    // 点赞功能

    // 获取所有的小爱心元素
    var likes = document.querySelectorAll(".like");
    console.log(likes)
    // 遍历每个小爱心元素
    likes.forEach(function (like) {
        // 为每个小爱心元素添加一个 click 事件监听器
        like.addEventListener("click", function () {
            // 阻止事件冒泡到父元素
            event.stopPropagation();
            // 切换小爱心元素的 active 类
            // like.classList.toggle("active");
            if (like.classList.contains("active")) {
                // "active" class已经存在，执行移除命令
                like.classList.remove("active");
                var operate = "取消点赞"
            } else {
                // "active" class不存在，执行添加命令
                like.classList.add("active");
                var operate = "点赞"
            }
            // 获取小爱心元素的 data-id 属性，即文件名
            var food_name = like.getAttribute("data-id");
            // 创建一个 AJAX 请求对象
            var xhr = new XMLHttpRequest();
            // 设置请求的方法和地址，比如 /like/ 文件名
            xhr.open("GET", "/like/" + food_name + "/" + operate);
            // 发送请求
            xhr.send();
        });
    });

    // 图片翻转效果
    // 获取所有的flip-box元素
    var flipBoxes = document.getElementsByClassName("flip-box");

    // 遍历每个flip-box元素
    for (var i = 0; i < flipBoxes.length; i++) {
        // 给每个flip-box元素添加一个点击事件
        flipBoxes[i].addEventListener("click", function () {
            // 获取当前点击的flip-box元素的子元素flip-box-inner
            var flipBoxInner = this.children[0];
            // 获取当前flip-box-inner元素的旋转角度
            var angle = flipBoxInner.style.transform;
            // 如果当前没有旋转，就旋转180度
            if (angle == "") {
                flipBoxInner.style.transform = "rotateY(180deg)";
            } else {
                // 如果当前已经旋转了180度，就恢复原样
                flipBoxInner.style.transform = "";
            }
        });
    }


});
