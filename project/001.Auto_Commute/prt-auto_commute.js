/* 사용법 */
/* 인터넷 브라우저 개발자 도구 > 콘솔에서 실행 */

/* 설정 */
var user_id = 'gwkim';
var user_pw = 'ahsgjs&3g';
var user_nm = '김건우';
var telegram = {'token': '6038387779:AAHGGLhhKcIxCN2BStwr_1FxKcSqa0hgnNc',
                'name': 'nu_1_bot',
                'chatId': ''
}
var tlgr_msg_dict = {'success': '출근 등록하였습니다.',
                'fail': '출근 등록하지 못 했습니다.'
}

/* 로그인 */
location.href="https://ngwx.ktbizoffice.com/LoginN.aspx?compid=iteyes";
document.getElementById('TextUserID').value = user_id;
document.getElementById('TextPassword').value = user_pw;
document.getElementById('LoginButton').click();

/* 그룹웨어 메인 */
/* https://ngwx.ktbizoffice.com/myoffice/ezportal/index_portal_Cross.aspx */

/* 출근입력 */
var isOff = false;
var time_interval_to_execute = Math.ceil(Math.random() * (9000 * 10));
var ul = document.querySelector('#mainFrame').contentWindow.document.querySelector('#subtdde08 > iframe').contentWindow.document.querySelector('#tdResultList > ul');

for (var li of ul.children) {
    if (li.textContent.search(user_nm) > 0) {
        isOff = true;
        console.log('isOff >> ', isOff)
    }
}
console.log('1>>>> ', time_interval_to_execute)
setTimeout(function(isOff) {
    if (isOff) {
        if ($('#disIN').textContent === '출근입력') {
            /* $('#disIN').click(); */
            console.log('2>>>> ', time_interval_to_execute);
        }
    }
}, time_interval_to_execute);

