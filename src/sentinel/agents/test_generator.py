"""Test Generator Agent using LangChain and Azure OpenAI"""

from typing import Dict, List, Optional

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.tools import Tool
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_agent_executor

from sentinel.core.config import settings
from sentinel.core.logging import get_logger

logger = get_logger(__name__)


class TestGeneratorAgent:
    """AI agent for generating test code based on context"""
    
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.3,
        )
        
        self.system_prompt = """You are an expert test automation engineer specializing in creating comprehensive test suites.
        
        Your responsibilities:
        1. Analyze code changes and requirements to generate appropriate tests
        2. Create E2E tests using Cypress for UI changes
        3. Create integration tests using pytest for API changes
        4. Generate regression tests for bug fixes
        5. Ensure tests follow best practices and are maintainable
        
        Always generate executable test code that follows the project's conventions.
        Include clear assertions and avoid hard-coded waits.
        """
        
        self._setup_tools()
        self._setup_agent()
    
    def _setup_tools(self):
        """Setup tools available to the agent"""
        # TODO: Add actual tools for:
        # - Fetching code diffs
        # - Reading existing tests
        # - Analyzing component structure
        # - Validating test syntax
        self.tools = []
    
    def _setup_agent(self):
        """Setup the agent with prompts and tools"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # For now, create a simple chain without tools
        self.agent = prompt | self.llm
    
    async def generate_tests(
        self,
        code_diff: str,
        jira_context: Optional[Dict] = None,
        existing_tests: Optional[List[str]] = None,
        test_types: List[str] = ["e2e", "integration"]
    ) -> Dict[str, str]:
        """Generate tests based on code changes and context"""
        
        logger.info("Generating tests", extra={
            "test_types": test_types,
            "has_jira_context": bool(jira_context),
            "has_existing_tests": bool(existing_tests)
        })
        
        # Build context for the agent
        context_parts = [f"Code changes:\n{code_diff}"]
        
        if jira_context:
            context_parts.append(f"\\nUser Story: {jira_context.get('summary', '')}")
            context_parts.append(f"Acceptance Criteria: {jira_context.get('acceptance_criteria', '')}")
        
        if existing_tests:
            context_parts.append(f"\\nExisting tests to consider:\\n{chr(10).join(existing_tests[:3])}")
        
        context = "\n\n".join(context_parts)
        
        # Generate tests for each type
        generated_tests = {}
        
        for test_type in test_types:
            prompt = f"""Based on the following context, generate {test_type} tests:
            
            {context}
            
            Generate executable test code for {test_type} testing.
            """
            
            response = await self.agent.ainvoke({"input": prompt})
            generated_tests[test_type] = response.content
        
        return generated_tests
    
    async def validate_test_code(self, test_code: str, test_type: str) -> Dict[str, any]:
        """Validate generated test code"""
        
        prompt = f"""Validate the following {test_type} test code:
        
        {test_code}
        
        Check for:
        1. Syntax errors
        2. Missing imports
        3. Undefined variables or functions
        4. Best practices violations
        
        Return a JSON with: {{"valid": boolean, "issues": [], "suggestions": []}}
        """
        
        response = await self.agent.ainvoke({"input": prompt})
        
        # TODO: Parse and return structured validation results
        return {"valid": True, "issues": [], "suggestions": []}