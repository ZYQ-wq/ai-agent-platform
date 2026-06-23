import request from "@/utils/request";

export const getAgents = () => {
  return request.get(
    "/agents/my"
  );
};