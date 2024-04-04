/**
 * 配置cookie
 * @author Cerelise-wong
 */
import { useCookies } from "@vueuse/integrations/useCookies";

const TokenKey = "jobs-token";
const cookie = useCookies();

export function getToken() {
	return cookie.get(TokenKey);
}

export function setToken(token) {
	return cookie.set(TokenKey, token);
}

export function removeToken() {
	console.log("Removing token");
	return cookie.remove(TokenKey);
}
