import Header from './components/Header/Header';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import {DiscussionsMain} from "./pages/DiscussionsPages/DiscussionsMain";
import {Main} from "./pages/Main";
import {PublicArticle} from "./pages/ArticlesPages/PublicArticle";
import {Login} from "./pages/UserPages/Login";
import {Register} from "./pages/UserPages/Register";
import {Logout} from "./pages/UserPages/Logout";
import {AuthProvider, useAuth} from "./contexts/AuthContext";
import ArticlePage from "./pages/ArticlesPages/ArticlePage";
import {Profile} from "./pages/UserPages/Profile";
import ThreadList from "./components/ThreadList";
import CommentList from "./components/CommentList";
import GroupList from "./components/GroupList";
import CreateComment from "./components/CreateComment";
import CreateThread from "./components/CreateThread";
import CreateGroup from "./components/CreateGroup";

function App() {

    return (
        <AuthProvider>
            <Router>
                <Header />
                <Routes>
                    <Route path="/" element={<Main />} />
                    <Route path="/public" element={<PublicArticle />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/logout" element={<Logout />} />
                    <Route path="/article/:article_id" element={<ArticlePage />} />
                    <Route path="/profile" element={<Profile />} />
                    <Route path="/profile/:userId" element={<Profile />} />
                    <Route path="/discussions" element={<GroupList />} />
                    <Route path="/groups/:groupId/threads" element={<ThreadList />} />
                    <Route path="/threads/:threadId/comments" element={<CommentList />} />
                    <Route path="/create-group" element={<CreateGroup />} />
                    <Route path="/groups/:groupId/threads/create" element={<CreateThread />} />
                    <Route path="/threads/:threadId/comments/create" element={<CreateComment />} />
                </Routes>
            </Router>
        </AuthProvider>

    );
}

export default App;
