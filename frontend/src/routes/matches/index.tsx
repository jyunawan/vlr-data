import { createFileRoute, Link } from "@tanstack/react-router";
import useFetch from "@hooks/useFetch";
import type { Match } from "@/types";
import { timeUntil } from "@/utils/timeUntil";

export const Route = createFileRoute("/matches/")({
  component: RouteComponent,
});

function RouteComponent() {
  const {
    data: matches,
    loading: matches_loading,
    error: matches_error,
  } = useFetch<Match[]>("http://localhost:8000/api/upcoming_matches");

  if (matches_loading) return <div>Loading…</div>;
  if (matches_error) return <div>Error: {matches_error}</div>;

  if (!matches) {
    // covers both null and undefined
    return <div>No data yet</div>;
  }

  return (
    <div className="mx-5 my-3">
      <h1>Upcoming</h1>
      <div className="flex flex-col gap-3 bg-gray-950">
        {matches.map((match) => {
          const { days, hours, minutes } = timeUntil(
            new Date(match.date_played),
          );

          return (
            <Link to="/matches/$matchId" params={{ matchId: match.vlr_id }} key={match.vlr_id}>
              <div className="flex flex-col items-center rounded-2xl border-1 border-gray-900">
                <div className="mt-3 text-lg font-medium text-gray-300">
                  {(days > 0 || hours > 0) &&
                    "Starting in: " + days + "d " + hours + "h"}

                  {minutes > 0 &&
                    days <= 0 &&
                    hours <= 0 &&
                    "Starting in: " + minutes + " minutes"}

                  {days <= 0 && hours <= 0 && minutes <= 0 && "Game Started"}
                </div>

                <div className="mb-4 grid w-full grid-cols-3 items-center px-5 text-xl">
                  <div className="flex -translate-y-3 items-center justify-start gap-3">
                    <div className="aspect-square size-12 rounded-full bg-white px-2 py-2">
                      <img
                        src={match.team1_logo}
                        alt={match.team1}
                        className="h-full w-full object-contain"
                      />
                    </div>
                    {match.team1}
                  </div>

                  <div className="justify-self-center text-3xl">VS</div>

                  <div className="flex -translate-y-3 items-center justify-end gap-3">
                    {match.team2}
                    <div className="aspect-square size-12 rounded-full bg-white px-2 py-2">
                      <img
                        src={match.team2_logo}
                        alt={match.team2}
                        className="h-full w-full object-contain"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
