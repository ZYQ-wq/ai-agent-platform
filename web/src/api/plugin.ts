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

export const createFile = (
  projectId: string,
  path: string
) => {
  return request.post(
    `/plugins/${projectId}/files`,
    {
      path,
      language: "plaintext"
    }
  );
};

export const renameFile = (
  fileId: string,
  path: string
) => {

  return request.put(
    `/plugins/files/${fileId}/rename`,
    {
      path
    }
  );

};

export const deleteFile = (
  fileId: string
) => {

  return request.delete(
    `/plugins/files/${fileId}`
  );

};

export const validateManifest = (
  projectId: string
) => {

  return request.get(
    `/plugins/${projectId}/manifest`
  );

};

export const editCode = (
  content: string,
  prompt: string
) => {
  return request.post(
    "/plugins/edit",
    {
      content,
      prompt
    }
  );
};

export const bindAgent = (
  projectId: string,
  agentId: number | null
) => {

  if (agentId === null) {

    return request.put(
      `/plugins/${projectId}/agent/unbind`
    );

  }

  return request.put(
    `/plugins/${projectId}/agent/${agentId}`
  );

};
