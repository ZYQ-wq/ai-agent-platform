import request, {
  LONG_REQUEST_TIMEOUT
} from "@/utils/request";

export const generateCode = (
  projectId: string,
  prompt: string
) => {
  return request.post(
    "/plugins/generate",
    {
      project_id: projectId,
      prompt
    },
    {
      timeout: LONG_REQUEST_TIMEOUT
    }
  );
};