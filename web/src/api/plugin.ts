import request, {
  LONG_REQUEST_TIMEOUT
} from "../utils/request";

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
    `/plugins/${projectId}/run`,
    undefined,
    {
      timeout: LONG_REQUEST_TIMEOUT
    }
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
    },
    {
      timeout: LONG_REQUEST_TIMEOUT
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

export const agentChat = (
  projectId: string,
  prompt: string
) => {

  return request.post(
    "/plugins/agent",
    {
      project_id: projectId,
      prompt
    },
    {
      timeout: LONG_REQUEST_TIMEOUT
    }
  );

};

export const applyChanges = (
  projectId: string,
  files: any[]
) => {

  return request.post(
    "/plugins/apply",
    {
      project_id: projectId,
      files
    }
  );

};

