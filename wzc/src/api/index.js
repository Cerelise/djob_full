import request from "./request";

export const loginApi = (user) => request.post("/auth/user/login", user);
export const registerApi = (user) => request.post("/auth/user/register", user);
export const editUserinfoApi = (params) => request.post("auth/user/me", params);
export const sendVerifyEmail = (params) =>
	request.post("auth/user/verify", params);

export const getUsersApi = (pager) => request.get("/manager/user/list", pager);
export const createUserApi = (user) => request.post("/manager/user/list", user);
export const deleteUserApi = (id) =>
	request.delete("/manager/user/detail/" + id);

export const getApprovalsApi = (keyword) =>
	request.get("/manager/cj-list", { keyword });
export const passJobApi = (id, params) =>
	request.post("/manager/verify/job/" + id, params);
export const passCompApi = (id, params) =>
	request.post("/manager/verify/company/" + id, params);

export const deleteCommentApi = (params) =>
	request.delete("/manager/comment/detail", params);
export const publishCommentApi = (id, params) =>
	request.post("/jobs/" + id + "/comment-area", params);
export const getComments = () => request.get("/manager/comment");
export const sendApplyApi = (id) => request.post("/jobs/" + id + "/apply");

export const getUserinfoApi = () => request.get("/auth/user/me");
export const getUserApplyApi = () => request.get("/notification");
export const getTagsApi = () => request.get("jobs/category");

export const createCompApi = (params) =>
	request.post("company/cp-list", params);
export const uploadCompLogoApi = (params) =>
	request.post("company/cp/picture", params);
export const getCompInfoApi = (id) => request.get("company/detail", { id });

export const getAppliesUserApi = () => request.get("auth/user/apply");
export const getAppliesEmployerApi = () =>
	request.get("auth/user/apply-employer");

export const getJobsApi = (params) => request.get("/jobs/stats", params);
export const getJobInfoApi = (id) => request.get("/jobs/job-detail/" + id);
export const createJobApi = (params) => request.post("/jobs/job-list", params);

export const passUserApplyApi = (id, status) =>
	request.put("/jobs/apply-detail/" + id, { status });
