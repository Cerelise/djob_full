/**
 * Storage二次封装
 * @author Cerelise-wong
 */
import { NAME_SPACE } from "@/config";
export default {
	setItem(key, val) {
		let storage = this.getStorage();
		console.log(val);
		storage[key] = val;
		window.localStorage.setItem(NAME_SPACE, JSON.stringify(storage));
	},
	getItem(key) {
		return this.getStorage()[key];
	},
	getStorage() {
		return JSON.parse(window.localStorage.getItem(NAME_SPACE) || "{}");
	},
	clearItem(key) {
		let storage = this.getStorage();
		delete storage[key];
		window.localStorage.setItem(NAME_SPACE, JSON.stringify(storage));
	},
	clearAll() {
		window.localStorage.clear();
	},
};
