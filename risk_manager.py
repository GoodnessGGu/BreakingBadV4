import logging
import time
from datetime import datetime, date
from settings import config

logger = logging.getLogger(__name__)

class RiskManager:
    """
    Manages risk limits such as Daily Stop Loss and Max Drawdown.
    """
    def __init__(self):
        self.daily_pnl = 0.0
        self.daily_wins = 0
        self.daily_losses = 0
        self.last_reset_date = date.today()
        # Default stop loss from config could be used, or set dynamically
        self.daily_stop_loss = 0.0 # 0.0 means disabled by default unless set

    def _check_reset(self):
        """Resets counters if a new day has started."""
        if date.today() > self.last_reset_date:
            logger.info(f"🔄 RiskManager: New day detected. Resetting Daily PnL (Prev: ${self.daily_pnl:.2f})")
            self.daily_pnl = 0.0
            self.daily_wins = 0
            self.daily_losses = 0
            self.last_reset_date = date.today()

    def update_trade_result(self, pnl: float):
        """
        Updates the daily PnL based on a closed trade.
        """
        self._check_reset()
        self.daily_pnl += pnl
        
        if pnl > 0:
            self.daily_wins += 1
        else:
            self.daily_losses += 1
            
        logger.info(f"📊 RiskManager: Daily PnL updated: ${self.daily_pnl:.2f} (Wins: {self.daily_wins} | Losses: {self.daily_losses})")

    def can_trade(self) -> tuple[bool, str]:
        """
        Checks if trading is allowed based on risk limits.
        
        Returns:
            (bool, str): (Allowed, Reason)
        """
        self._check_reset()
        
        # Check Stop Loss (if enabled)
        # config.daily_stop_loss should be a positive number (e.g., 15.0)
        # If daily_pnl is below -15.0, stop.
        limit = getattr(config, 'daily_stop_loss', 0.0)
        if limit > 0 and self.daily_pnl <= -limit:
            msg = f"🛑 Daily Stop Loss Hit! Current PnL: ${self.daily_pnl:.2f} (Limit: -${limit:.2f})"
            return False, msg
            
        return True, "OK"

    def get_status(self):
        self._check_reset()
        limit = getattr(config, 'daily_stop_loss', 0.0)
        status = "🟢 Active" if (limit == 0 or self.daily_pnl > -limit) else "🔴 STOPPED"
        return f"Daily PnL: ${self.daily_pnl:.2f}\nStop Loss: -${limit:.2f}\nStatus: {status}"

# Global Instance
risk_manager = RiskManager()
