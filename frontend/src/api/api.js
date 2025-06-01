import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000", // адрес backend FastAPI
});

// Groups
export const fetchGroups = () => API.get("/discussion-service/groups/");
export const createGroup = (data) => API.post("/discussion-service/groups/", data);

// Threads
export const fetchThreads = (groupId) => API.get(`/discussion-service/threads/group/${groupId}`);
export const createThread = (data) => API.post("/discussion-service/threads/", data);

// Comments
export const fetchComments = (threadId) => API.get(`/discussion-service/comments/thread/${threadId}`);
export const createComment = (data) => API.post("/discussion-service/comments/", data);

export default API;
