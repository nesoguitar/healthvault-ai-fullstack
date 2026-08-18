"use client";

import { useQuery } from "@tanstack/react-query";
import { timelineApi } from "@/lib/api/resources";

export function useTimeline() {
  return useQuery({
    queryKey: ["timeline"],
    queryFn: timelineApi.list,
  });
}
