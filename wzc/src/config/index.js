export const BASE_URL = "http://127.0.0.1:8000/";
export const NAME_SPACE = "job";

export const RULES = {
	username: {
		required: true,
		message: "请输入用户名",
		trigger: "blur",
	},
	password: [
		{
			required: true,
			message: "请输入密码",
			trigger: "blur",
		},
		{
			required: true,
			min: 8,
			message: "最短长度为 8",
		},
	],
	reenteredPassword: [
		{
			required: true,
			message: "请再次输入密码",
			trigger: ["input", "blur"],
		},
		{
			required: true,
			min: 8,
			message: "最短长度为 8",
		},
	],
	email: {
		required: true,
		message: "请输入正确的邮箱地址",
		trigger: "blur",
		validator: (rule, value) => {
			return Boolean(
				/^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/.test(value)
			);
		},
	},
	code: {
		required: true,
		message: "验证码不能为空",
		trigger: "blur",
	},
};
export const COMP_RULES = {
	title: {
		required: true,
		message: "请输入公司名称",
		trigger: "blur",
	},
	address: {
		required: true,
		message: "该字段不能为空",
		trigger: "blur",
	},
};

export const JOB_RULES = {
	title: {
		required: true,
		message: "该字段不能为空",
		trigger: "blur",
	},
};
