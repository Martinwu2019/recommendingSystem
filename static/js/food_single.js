document.addEventListener('DOMContentLoaded', function() {
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
});