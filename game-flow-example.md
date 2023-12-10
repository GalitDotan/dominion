# Game Initiation
* Request: `NewGame(player_name=SIRI)` -> `game_id = game-1234`
* Request: `JoinGame(player_name=LIBI, game_id='game-1234')`
* Request: `JoinGame(player_name=RIKI, game_id='game-1234')`
* Request: `StartGame(game_id='game-1234')`

# Game run
* Effect: `GameSetup()`
    * Effect: `Draw(SIRI, 5)`
        * Note: Draw does shuffle and put discard in draw pile
                when no cards in draw pile
    * Effect: `Draw(LIBI, 5)`
    * Effect: `Draw(RIKI, 5)`
* Effect: `TurnStart(SIRI)`
    * Effect: `ActionPhase(SIRI)`
      * 
    * Effect: `BuyPhase(SIRI)`
    * Effect: `NightPhase(SIRI)`
    * Effect: `CleanUpPhase(SIRI)`