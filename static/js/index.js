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