import React, { useEffect, useState } from "react";
import { fetchGroups } from "../api/api";
import { Link } from "react-router-dom";
import "./GroupList.css";

export default function GroupList() {
  const [groups, setGroups] = useState([]);

  useEffect(() => {
    fetchGroups().then(res => setGroups(res.data));
  }, []);

  return (
    <div className="grouplist-container">
      <h2 className="grouplist-title">Группы</h2>
      <ul className="grouplist-list">
        {groups.map(group => (
          <li key={group.id} className="grouplist-item">
            <Link to={`/groups/${group.id}/threads`} className="grouplist-link">
              {group.title} ({group.member_count})
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
