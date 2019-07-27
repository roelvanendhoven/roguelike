import uuid
import json
import constants as c

from components.map import Map


class SessionManager:
    sessions = []

    def on_lobby_event(self, player, event):
        if event['action'] is 'host':
            self.host_session(player, event['dungeon_id'])
        elif event['action'] is 'get':
            sessions = self.get_sessions_for_dungeon(event['dungeon_id'])
            player.send((c.LOBBIES, {'response': 'get', "sessions": self._serialize_sessions(sessions)}))
        elif event['action'] is 'get-all':
            player.send((c.LOBBIES, {'response': 'get', "sessions": self._serialize_sessions(self.sessions)}))
        elif event['action'] is 'join':
            self.join_session(player, event['id'])
        elif event['action'] is 'ready':
            self.ready_session(player, event['id'], event['value'])
        elif event['action'] is 'leave':
            self.leave_session(player, event['id'])

        self.show_all_sessions_data()

    def on_player_intent(self, player, intent):
        session = self.get_session(intent.id)
        session.player_intent(player, intent.action)

    def get_session(self, session_id):
        for s in self.sessions:
            if s.id is session_id:
                return s

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

    def host_session(self, player, dungeon_id):
        session = Session(player, dungeon_id)
        self.sessions.append(session)

    def join_session(self, player, session_id):
        session = self.get_session(session_id)
        session.join(player)

    def ready_session(self, player, session_id, value):
        session = self.get_session(session_id)
        session.ready(player, value)

    def leave_session(self, player, session_id):
        session = self.get_session(session_id)
        session.leave(player)
        if not session.players:
            self.sessions.remove(player)

    def _serialize_sessions(self, sessions):
        result = []
        for s in sessions:
            result.append(s.serialize())
        return json.dumps(result)

    def show_all_sessions_data(self):
        for s in self.sessions:
            print(s.serialize)


class Session:
    players = []

    def __init__(self, player, dungeon_id):
        self.id = uuid.uuid1()
        self.dungeon_id = dungeon_id
        self.players.append(player)
        self.map = Map(dungeon_id)

    def join(self, player):
        self.players.append(player)
        player.send((c.MAP, self.map.serialize()))
        self.send_to_all((c.LOBBIES, {'message': player.name + ' joined'}))

    def leave(self, player):
        self.players.remove(player)
        self.send_to_all((c.LOBBIES, {'message': player.name + ' left'}))

    def ready(self, player, value):
        player.is_ready = value

        if value:
            message = player.name + ' is ready'
        else:
            message = player.name + ' is not ready'

        self.send_to_all((c.LOBBIES, {'message': message}))

        for p in self.players:
            if not p.is_ready:
                return
        self._start()

    def _start(self):
        self.send_to_all((c.LOBBIES, {'start': 'True'}))

    def player_intent(self, player, action):
        print("player intent")
        # TODO: handle action
        # Do stuff
        # resolve_action(result)

    def resolve_action(self, result):
        self.send_to_all((c.PLAYER_RESOLVE, result))

    def serialize(self):
        return json.dumps({
            'id': self.id,
            'dungeon_id': self.dungeon_id,
            'players': [p.name for p in self.players]
        })

    def send_to_all(self, message):
        for p in self.players:
            p.send(message)
