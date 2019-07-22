import uuid
import json
import constants as c
from components.net_utils import send


class SessionManager:
    sessions = []

    def on_lobby_event(self, sock, event):
        if event.action is 'HOST':
            self.host_session(sock, event.dungeon_id)
        elif event.action is 'GET':
            sessions = self.get_sessions_for_dungeon(event.dungeon_id)
            send(sock, (c.LOBBIES, {self._serialize_sessions(sessions)}))
        elif event.action is 'GET-ALL':
            send(sock, (c.LOBBIES, {self._serialize_sessions(self.sessions)}))
        elif event.action is 'JOIN':
            self.join_session(sock, event.id)
        elif event.action is 'LEAVE':
            self.leave_session(sock, event.id)

    def on_player_intent(self, sock, intent):
        session = self.get_session(intent.id)
        session.player_intent(sock, intent.action)

    def get_session(self, session_id):
        for s in self.sessions:
            if s.id is session_id:
                return s.id

    def get_sessions_for_dungeon(self, dungeon_id):
        sessions = []
        for s in self.sessions:
            if s.dungeon_id is dungeon_id:
                sessions.append(s)
        if not sessions:
            return None
        return sessions

    def get_sessions_for_player(self, player):
        sessions = []
        for s in self.sessions:
            for p in s.players:
                if p is player:
                    sessions.append(s)
        if not sessions:
            return None
        return sessions

    def host_session(self, sock, dungeon_id):
        session = Session(sock, dungeon_id)
        self.sessions.append(session)

    def join_session(self, sock, session_id):
        self.get_session(session_id).join(sock)

    def leave_session(self, sock, session_id):
        session = self.get_session(session_id)
        session.leave(sock)
        if not session.players:
            self.sessions.remove(sock)

    def _serialize_sessions(self, sessions):
        result = []
        for s in sessions:
            result.append(s.serialize())
        return result


class Session:
    players = []

    def __init__(self, sock, dungeon_id):
        self.id = uuid.uuid1()
        self.dungeon_id = dungeon_id
        self.players.append(sock)

    def join(self, sock):
        self.players.append(sock)

    def leave(self, sock):
        self.players.remove(sock)

    def player_intent(self, sock, action):
        print("player intent")
        # TODO: handle action
        # Do stuff
        # resolve_action(result)

    def resolve_action(self, result):
        for p in self.players:
            send(p.socket, (c.PLAYER_RESOLVE, result))

    def serialize(self):
        return json.dumps({
            'id': self.id,
            'dungeon_id': self.dungeon_id,
            'players': [p.name for p in self.players]
        })
