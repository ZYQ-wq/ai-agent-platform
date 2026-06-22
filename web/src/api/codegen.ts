import request from "@/utils/request";

export const generateCode = (
  projectId: string,
  prompt: string
) => {
  return request.post(
    "/plugins/generate",
    {
      project_id: projectId,
      prompt
    }
  );
};