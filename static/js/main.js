// nav 높이 + contents 높이 + footer 높이 < viewport 높이
// : footer를 viewport 하단에 고정
// nav 높이 + contents 높이 + footer 높이 >= viewport 높이
// : footer의 fix 속성을 제거
let nav_h = document.querySelector('div.nav').clientHeight;
let con_h = document.querySelector('div#contents').clientHeight;
let footer_h = document.querySelector('footer').clientHeight;
console.log(nav_h, con_h, footer_h)
console.log(window.innerHeight)
doc_h = nav_h + con_h + footer_h;
if (doc_h >= window.innerHeight) {
    document.querySelector('footer').classList.remove('fixed-bottom')
}