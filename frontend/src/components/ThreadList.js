import React, { useEffect, useState } from "react";
import { fetchThreads } from "../api/api";
import { useParams, Link } from "react-router-dom";
import "./ThreadList.css";

export default function ThreadList() {
  const { groupId } = useParams();
  const [threads, setThreads] = useState([]);

  useEffect(() => {
    fetchThreads(groupId).then(res => setThreads(res.data));
  }, [groupId]);

  return (
    <div className="threadlist-container">
      <h2 className="threadlist-title">Треды группы</h2>
      <ul className="threadlist-list">
        {threads.map(thread => (
          <li key={thread.id} className="threadlist-item">
            <Link to={`/threads/${thread.id}/comments`} className="threadlist-link">
              {thread.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
