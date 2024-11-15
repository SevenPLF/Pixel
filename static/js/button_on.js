var timeout;

// 为每个选项卡绑定点击事件
document.querySelectorAll('.tab-button').forEach(function (tab) {
    tab.addEventListener('click', function () {
        // 移除所有选项卡的激活状态
        document.querySelectorAll('.tab-button').forEach(function (tab) {
            tab.classList.remove('active');
        });
        // 移除所有内容的激活状态
        document.querySelectorAll('.tab-content').forEach(function (content) {
            content.classList.remove('active');
        });

        // 添加激活状态到当前点击的选项卡和对应的内容
        var tabId = this.id.replace('tab-', '');
        document.getElementById('content-' + tabId).classList.add('active');
        this.classList.add('active');
    });
});
$(document).ready(function () {
    $('#searchForm').submit(function (e) {
        e.preventDefault(); // 防止表单提交
        var query = $('#searchInput').val();
        var csrftoken = $('input[name=csrfmiddlewaretoken]').val(); // 获取CSRF令牌
        $.ajax({
            url: '/search/', // 替换为你的搜索视图URL
            type: 'POST',
            data: {'q': query},
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                $('#searchResults').empty();
                $.each(data, function (index, item) {
                    var fullText = item.source + ' ' + item.name;
                    var displayText = fullText.length > 10 ? fullText.substring(0, 10) + '...' : fullText;

                    var li = $('<li>')
                        .attr('title', fullText) // 设置悬浮框内容为完整文本
                        .css('color', item.is_del === 0 ? 'red' : 'blue')
                        .hover(function() {
                            $(this).attr('title', fullText); // 鼠标悬停时显示完整内容
                        });

                    if (item.is_del === 0) {
                        li.css({
                            'text-decoration': 'line-through',
                            'opacity': '0.5'
                        });
                    }

                    li.text(displayText).appendTo('#searchResults');
                });
            }
        });
    });
});

function handleClick(button) {
    var existingPopovers = document.querySelectorAll('.popover');
    existingPopovers.forEach(function (popover) {
        popover.style.display = 'none';
    });
    var buttonId = button.getAttribute('data-id');
    var popoverId = 'popover-' + buttonId;
    var popover = document.getElementById(popoverId);
    if (popover) {
        document.body.removeChild(popover);
    }
    popover = document.createElement('div');
    popover.classList.add('popover');
    popover.id = popoverId;
    document.body.appendChild(popover);
    popover.style.display = 'block';
    var buttonRect = button.getBoundingClientRect();
    var pageX = buttonRect.left + button.offsetWidth / 2;
    var pageY = buttonRect.top + button.offsetHeight / 2;
    popover.style.top = (pageY - 170) + 'px';
    popover.style.left = (pageX) + 'px';
    var colorPicker = document.getElementById('colorPicker');
    var color = colorPicker.value;
    var textarea = document.createElement('textarea');
    var count_cc = document.createElement('div');
    count_cc.textContent = '1';
    count_cc.title = '当前图层';

    var person = document.getElementById('person');
    var profileContainer = document.getElementById('profileContainer');
    // 清除容器中的所有内容
    // profileContainer.innerHTML = '';
    // 创建新的内容
    var container = document.createElement('div');
    // 创建照片容器和图片
    var photoDiv = document.createElement('div');
    var photoImg = document.createElement('img');
    // 创建信息容器
    var infoDiv = document.createElement('div');
    // 创建姓名
    var nameH2 = document.createElement('h2');
    // 创建公司
    var companyP = document.createElement('p');
    // 创建地址
    var addressP = document.createElement('p');
    // 创建位置
    var locationP = document.createElement('p');
    // 创建电话
    var phoneP = document.createElement('p');
    container.className = 'container';
    textarea.placeholder = '输入文本';


    // 将照片和信息容器添加到容器中
    photoDiv.appendChild(photoImg);
    infoDiv.appendChild(nameH2);
    // companyP.className = 'company';
    // companyP.textContent = 'Shell, Inc.';
    infoDiv.appendChild(companyP);
    infoDiv.appendChild(addressP);
    infoDiv.appendChild(locationP);
    infoDiv.appendChild(phoneP);
    container.appendChild(photoDiv);
    container.appendChild(infoDiv);

    // 将容器添加到页面中
    profileContainer.appendChild(container);
    person.appendChild(profileContainer);
    // person.innerHTML = ''


    popover.appendChild(textarea);
    var charCount = document.createElement('div');
    charCount.classList.add('char-count');
    // charCount.textContent = '140字';
    charCount.textContent = '剩余:0小时';

    textarea.addEventListener('input', function () {
        var textLength = textarea.value.length;
        if (textLength > 140) {
            textarea.value = textarea.value.substring(0, 140);
            textLength = 140;
        }
        // charCount.textContent = (140 - textLength) + '字';
    });
    popover.appendChild(charCount);
    var cancelButton = document.createElement('button');
    cancelButton.textContent = '取消';
    cancelButton.classList.add('cancel-button');
    cancelButton.addEventListener('click', function () {
        popover.style.display = 'none';
    });
    var confirmButton = document.createElement('button');
    confirmButton.textContent = '确认';
    confirmButton.classList.add('confirm-button');

    var addButton = document.createElement('button');
    addButton.textContent = '延长时间';
    addButton.classList.add('confirm-button');
    addButton.title = '使用1积分延长格子一小时'
    var buttonContainer = document.createElement('div');
    buttonContainer.classList.add('button-container1');
    count_cc.classList.add('count-text');
    popover.appendChild(buttonContainer);
    buttonContainer.appendChild(confirmButton);
    buttonContainer.appendChild(cancelButton);
    buttonContainer.appendChild(count_cc);
    buttonContainer.appendChild(addButton);

    popover.appendChild(buttonContainer);

    $.ajax({
        url: '/api/get_label_data/' + buttonId + '/',
        method: 'GET',
        data: {
            'buttonId': buttonId,
            'color': color,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        success: function (response) {
            if (response.success) {
                charCount.textContent = '剩余:' + response.hours_difference + '小时';
                if (response.data[0] === '0') {
                    if (response.data[2].user_points > -1) {
                        button.style.backgroundColor = color;
                    } else {
                        textarea.placeholder = '白板绘图至少需要1积分，当前积分不足';
                    }
                    textarea.placeholder = '白板不支持输入文本，一个格子消耗一积分';
                    confirmButton.disabled = true;
                    confirmButton.classList.add('cancel-button');
                    // textarea.disabled = true
                    textarea.readOnly = true;
                    var locationP = document.getElementById('ji-fen');
                    var addressP = document.getElementById('jin-yan');
                    // 清除容器中的所有内容
                    locationP.innerHTML = '';
                    // var locationP = document.createElement('p');
                    locationP.className = 'location';
                    locationP.textContent = '积分:' + response.data[2].user_points;
                    addressP.innerHTML = '';
                    // var locationP = document.createElement('p');
                    addressP.className = 'address';
                    addressP.textContent = '经验:' + response.data[2].user_experience;
                }
                if (response.data[0] && response.data[0] !== '0') {
                    textarea.placeholder = response.data[0];
                    count_cc.textContent = response.data[1];
                } else {
                    count_cc.textContent = response.data[1];
                }
                if (response.data[1] >= 3 && response.data[0] !== '0') {
                    // 如果返回值大于等于3，禁用确认按钮
                    confirmButton.disabled = true;
                    confirmButton.classList.add('cancel-button');
                    textarea.disabled = true
                    textarea.readOnly = true;
                } else {
                    // 如果返回值小于3，启用确认按钮
                    confirmButton.disabled = false;
                    confirmButton.classList.add('confirm-button');
                }
                if (response.data[2] !== '0' && response.data[0] !== '0') {
                    document.getElementById('other_name').textContent = response.data[2];
                    document.getElementById('company').textContent = '';

                    var companyImage = document.getElementById('company');
                    companyImage.src = '';
                    switch (response.level) {
                      case 0:
                        companyImage.src = '/static/image/person.png';
                        break;
                      case 1:
                        companyImage.src = '/static/image/real_person.png';
                        break;
                      case 2:
                        companyImage.src = '/static/image/one_person.png';
                        break;
                      case 3:
                        companyImage.src = '/static/image/company.png';
                        break;
                      // 添加更多case来处理其他level值
                      default:
                        companyImage.src = '/static/image/person.png'; // 默认图片
                        break;
                    }
                    document.getElementById('is-realname-authenticated').textContent = '是否实名: ' + response.data[3].is_realname_authenticated;
                    document.getElementById('fans-count').textContent = '粉丝数量: ' + response.data[4];
                    document.getElementById('following-count').textContent = '关注数量: ' + response.data[5];
                    document.getElementById('follow-btn').textContent = response.data[6] ? '取消关注' : '关注';
                    document.getElementById('follow-btn').value = response.data[3].user_id + "_" + response.data[7] + "_" + response.data[4] + "_" + response.data[5];
                    document.getElementById('userAvatar1').src = response.url ? response.url : '/static/image/33.png';
                }
            } else {
                console.error('Error get_label_data:', response.error);
            }
        },
        error: function (xhr, status, error) {
            console.error('AJAX error:', error);
        }
    });

    confirmButton.addEventListener('click', function () {
        var text = textarea.value;
        var colorPicker = document.getElementById('colorPicker');
        var color = colorPicker.value;
        var lasttime = document.getElementById('last-time');
        var lasttime1 = lasttime.value;
        var csrftoken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

        $.ajax({
            url: '/api/process_data/' + buttonId + '/',
            method: 'POST',
            data: {
                'text': text,
                'color': color,
                'lasttime': lasttime1,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function (response) {
                if (response.success) {
                    button.style.backgroundColor = color;
                    popover.style.display = 'none';
                    var locationP = document.getElementById('ji-fen');
                    var addressP = document.getElementById('jin-yan');
                    // 清除容器中的所有内容
                    locationP.innerHTML = '';
                    // var locationP = document.createElement('p');
                    locationP.className = 'location';
                    locationP.textContent = '积分:' + response.data.user_points;
                    addressP.innerHTML = '';
                    // var locationP = document.createElement('p');
                    addressP.className = 'address';
                    addressP.textContent = '经验:' + response.data.user_experience;
                } else {
                    textarea.placeholder = '绘图至少需要1积分，当前积分不足';
                    console.error('Error processing data:', response.error);
                }
            },
            error: function (xhr, status, error) {
                console.error('AJAX error:', error);
            }
        });
    });

    // 延长时间
    addButton.addEventListener('click', function () {
        var csrftoken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

        $.ajax({
            url: '/api/add_button/' + buttonId + '/',
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            success: function (response) {
                if (response.success) {
                    popover.style.display = 'none';
                    var locationP = document.getElementById('ji-fen');
                    var addressP = document.getElementById('jin-yan');
                    // 清除容器中的所有内容
                    locationP.innerHTML = '';
                    // var locationP = document.createElement('p');
                    locationP.className = 'location';
                    locationP.textContent = '积分:' + response.data.user_points;
                    addressP.innerHTML = '';
                    // var locationP = document.createElement('p');
                    addressP.className = 'address';
                    addressP.textContent = '经验:' + response.data.user_experience;
                } else {
                    textarea.placeholder = '至少需要1积分，当前积分不足';
                    console.error('Error processing data:', response.error);
                }
            },
            error: function (xhr, status, error) {
                console.error('AJAX error:', error);
            }
        });

    });


    button.removeEventListener('mouseleave', function () {
        popover.style.display = 'none';
    });
    button.addEventListener('mouseleave', function () {
        clearTimeout(timeout);
    });
    popover.addEventListener('mouseover', function () {
        clearTimeout(timeout);
    });
}


document.body.addEventListener('mousemove', function (event) {
    var buttons = document.querySelectorAll('.button-grid button');
    var glowRadius = 20;
    buttons.forEach(function (button) {
        var buttonRect = button.getBoundingClientRect();
        var left = buttonRect.left;
        var top = buttonRect.top;
        var right = buttonRect.right;
        var bottom = buttonRect.bottom;
        if (event.clientX >= left - glowRadius && event.clientX <= right + glowRadius &&
            event.clientY >= top - glowRadius && event.clientY <= bottom + glowRadius) {
            button.classList.add('glow-button');
        } else {
            button.classList.remove('glow-button');
        }
    });
});

function toggleFollow() {
    var followBtn = document.getElementById('follow-btn');
    var followBtn_1 = followBtn.value.split("_")[0];
    var followBtn_2 = followBtn.value.split("_")[1];
    var isFollowed = followBtn.textContent;
    var csrftoken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
    $.ajax({
        url: '/api/followed_data/',
        method: 'POST',
        data: {
            'followBtn_1': followBtn_1,
            'followBtn_2': followBtn_2,
            'isFollowed': isFollowed,
            'csrfmiddlewaretoken': csrftoken
        },
        success: function (response) {
            if (response.success) {
                if (response.data.isFollowedflag) {
                    document.getElementById('fans-count').textContent = '粉丝数量: ' + (parseInt(followBtn.value.split("_")[2], 10) - 1).toString();
                    document.getElementById('following-count').textContent = '关注数量: ' + parseInt(followBtn.value.split("_")[3], 10).toString();
                    document.getElementById('follow-btn').textContent = '关注';
                    document.getElementById('follow-btn').value = followBtn_1 + "_" + followBtn_2 + "_" + (parseInt(followBtn.value.split("_")[2], 10) - 1).toString() + "_" + followBtn.value.split("_")[3];
                } else {
                    document.getElementById('fans-count').textContent = '粉丝数量: ' + (parseInt(followBtn.value.split("_")[2], 10) + 1).toString();
                    document.getElementById('following-count').textContent = '关注数量: ' + parseInt(followBtn.value.split("_")[3], 10).toString();
                    document.getElementById('follow-btn').textContent = '取消关注';
                    document.getElementById('follow-btn').value = followBtn_1 + "_" + followBtn_2 + "_" + (parseInt(followBtn.value.split("_")[2], 10) + 1).toString() + "_" + followBtn.value.split("_")[3];
                }
            }
        },
        error: function (xhr, status, error) {
            console.error('AJAX error:', error);
        }
    });
}

