import axios from "axios";
import { getToken, removeToken } from "@/utils/auth";
import { BASE_URL } from "@/config";
import { toast } from "@/utils";
import storage from "@/utils/storage";
import { router } from "../router";

const service = axios.create({
	baseURL: BASE_URL + "api",
	timeout: 10000,
});
// 添加headers
service.interceptors.request.use((config) => {
	const token = getToken();
	if (token) config.headers["Authorization"] = "Bearer " + token;
	return config;
});
// 处理输出结果，制定输出内容
service.interceptors.response.use(
	(res) => {
		console.log(res);
		const { data, msg, code } = res.data;
		if (msg) toast(msg);
		return data;
	},
	(err) => {
		console.log(err);
		if (err.response.data.code == "token_not_valid") {
			toast("token已过期，正在跳转登录页面", "error");
			removeToken();
			storage.clearAll();
			setTimeout(() => router.push("/login"), 3000);
		} else toast(err.message, "error");
	}
);
// 自定义请求
function request(options) {
	options.method = options.method || "get";
	if (options.method.toLowerCase() === "get") {
		options.params = options.data;
	}
	return service(options);
}

["get", "post", "put", "delete", "patch"].forEach((item) => {
	request[item] = (url, data, options) => {
		return request({
			url,
			data,
			method: item,
			...options,
		});
	};
});

export default request;
