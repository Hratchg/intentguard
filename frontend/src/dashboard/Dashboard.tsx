import { useState } from "react";
import { UserSidebar } from "./UserSidebar";
import { UserPanel } from "./UserPanel";

interface DashboardProps {
  initialScenario?: string;
}

export function Dashboard({ initialScenario }: DashboardProps) {
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null);

  return (
    <div className="flex h-[700px] border border-gray-800 rounded-xl overflow-hidden bg-gray-950">
      <UserSidebar
        selectedId={selectedUserId}
        onSelect={setSelectedUserId}
        initialScenario={initialScenario}
      />
      {selectedUserId ? (
        <UserPanel userId={selectedUserId} />
      ) : (
        <div className="flex-1 flex items-center justify-center text-gray-600">
          Select a user to inspect
        </div>
      )}
    </div>
  );
}
