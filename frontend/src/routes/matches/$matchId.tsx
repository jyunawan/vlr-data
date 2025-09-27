import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/matches/$matchId")({
  component: RouteComponent,
  loader: async ({ params }) => {
    return {
      matchId: params.matchId,
    };
  },
});

function RouteComponent() {
  const { matchId } = Route.useLoaderData();
  return <div>Hello "/matches/{matchId}"!</div>;
}
