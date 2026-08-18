"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { documentsApi } from "@/lib/api/resources";

export function useDocuments() {
  return useQuery({
    queryKey: ["documents"],
    queryFn: documentsApi.list,
    refetchInterval: (query) => {
      // Poll while any document is still "processing" so the table reflects
      // the async extraction pipeline completing, without the user reloading.
      const docs = query.state.data;
      return docs?.some((d) => d.status === "processing") ? 2500 : false;
    },
  });
}

export function useUploadDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (file: File) => documentsApi.upload(file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
    },
  });
}
