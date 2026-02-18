import type { Event } from "../api/types";

const EVENT_COLORS: Record<string, string> = {
  page_view: "#60a5fa",
  api_call: "#a78bfa",
  login: "#34d399",
  payment: "#fbbf24",
  support_ticket: "#f87171",
  search: "#38bdf8",
  feature_use: "#818cf8",
  error: "#ef4444",
  signup: "#4ade80",
  message_sent: "#fb923c",
};

interface TimelineViewProps {
  events: Event[];
}

export function TimelineView({ events }: TimelineViewProps) {
  return (
    <div className="overflow-x-auto">
      <div className="flex items-start gap-1 min-w-max py-4 px-2">
        {events.map((event) => (
          <div key={event.event_id} className="group relative flex flex-col items-center">
            <div
              className="w-3 h-3 rounded-full cursor-pointer hover:scale-150 transition-transform"
              style={{ backgroundColor: EVENT_COLORS[event.event_type] || "#6b7280" }}
            />
            <div className="absolute bottom-full mb-2 hidden group-hover:block z-10">
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-xs shadow-xl min-w-48">
                <div className="font-semibold text-gray-100">{event.event_type}</div>
                <div className="text-gray-400 mt-1">
                  {new Date(event.timestamp).toLocaleString()}
                </div>
                {Object.keys(event.properties).length > 0 && (
                  <pre className="text-gray-500 mt-1 text-[10px]">
                    {JSON.stringify(event.properties, null, 2)}
                  </pre>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="flex gap-3 flex-wrap px-2 mt-2">
        {Object.entries(EVENT_COLORS).map(([type, color]) => (
          <div key={type} className="flex items-center gap-1 text-[10px] text-gray-500">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />
            {type}
          </div>
        ))}
      </div>
    </div>
  );
}
