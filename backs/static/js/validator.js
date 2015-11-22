//validator
$.extend($.fn.validatebox.defaults.rules, {
	inrpwd: {
		validator: function(value, param) {
			return '' != $(param[0]).val();
		},
		message: '请重复输入密码'
	},
	equals: {
		validator: function(value, param) {
			return value == $(param[0]).val();
		},
		message: '重复密码不一致'
	},
	mobile: {
		validator: function(value, param) {
			return /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/i.test(value);
		},
		message: '手机号码格式错误'
	}
});