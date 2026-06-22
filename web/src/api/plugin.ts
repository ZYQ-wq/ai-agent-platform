import request from "../utils/request";

export const createProject = (data: any) => {
  return request.post("/plugins", data);
};

export const getProjects = () => {
  return request.get("/plugins");
};

export const getProjectFiles = (
  projectId: string
) => {
  return request.get(
    `/plugins/${projectId}/files`
  );
};

export const updateFile = (
  fileId: string,
  content: string
) => {
  return request.put(
    `/plugins/files/${fileId}`,
    {
      content
    }
  );
};

export const runProject = (
  projectId: string
) => {
  return request.post(
    `/plugins/${projectId}/run`
  );
};