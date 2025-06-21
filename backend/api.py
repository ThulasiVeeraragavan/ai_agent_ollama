from livekit.agents import llm
import enum
from typing import Annotated
import logging
from db_driver import DatabaseDriver

logger = logging.getLogger("user-data")
logger.setLevel(logging.INFO)

DB = DatabaseDriver()

class LoanDetails(enum.Enum):
    Loanid = "loanid"
    Amount = "amount"
    Date = "date"
    Pending = "pending"
    

class AssistantFnc(llm.FunctionContext):
    def __init__(self):
        super().__init__()
        
        self._loan_details = {
            LoanDetails.Loanid: "",
            LoanDetails.Amount: "",
            LoanDetails.Date: "",
            LoanDetails.Pending: ""
        }
    
    def get_loan_str(self):
        loan_str = ""
        for key, value in self._loan_details.items():
            loan_str += f"{key}: {value}\n"
            
        return loan_str
    
    @llm.ai_callable(description="lookup a loan by its loanid")
    def lookup_loan(self, loanid: Annotated[str, llm.TypeInfo(description="The loanid of the loan to lookup")]):
        logger.info("lookup loan - loanid: %s", loanid)
        
        result = DB.get_loan_by_loanid(loanid)
        if result is None:
            return "loan not found"
        
        self._loan_details = {
            LoanDetails.Loanid: result.loanid,
            LoanDetails.Amount: result.amount,
            LoanDetails.Date: result.date,
            LoanDetails.Pending: result.pending
        }
        
        return f"The loan details are: {self.get_loan_str()}"
    
    @llm.ai_callable(description="get the details of the current loan")
    def get_loan_details(self):
        logger.info("get loan  details")
        return f"The loan details are: {self.get_loan_str()}"
    
    @llm.ai_callable(description="create a new loan")
    def create_loan(
        self, 
        loanid: Annotated[str, llm.TypeInfo(description="The loanid of the loan")],
        amount: Annotated[str, llm.TypeInfo(description="The amount of the loan ")],
        date: Annotated[str, llm.TypeInfo(description="The date of the loan")],
        pending: Annotated[int, llm.TypeInfo(description="The pending of the loan")]
    ):
        logger.info("create loan - loanid: %s, amount: %s, date: %s, pending: %s", loanid, amount, date, pending)
        result = DB.create_loan(loanid, amount, date, pending)
        if result is None:
            return "Failed to create loan"
        
        self._loan_details = {
            LoanDetails.Loanid: result.loanid,
            LoanDetails.Amount: result.amount,
            LoanDetails.Date: result.date,
            LoanDetails.Pending: result.pending
        }
        
        return "loan created!"
    
    def has_loan(self):
        return self._loan_details[LoanDetails.Loanid] != ""