from datetime import timedelta
from typing import List, Dict, Any
from temporalio import workflow

@workflow.defn
class PodcastCreationWorkflow:
    @workflow.run
    async def run(self, tenant_id: str, topic: str) -> Dict[str, Any]:
        """
        Podcast Creation Workflow:
        1. Research topic.
        2. Generate script.
        3. Synthesize audio.
        """
        # Step 1: Research
        research_results = await workflow.execute_activity(
            "google_search_activity",
            args=[tenant_id, topic],
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        # Step 2: Generate Script
        script_output = await workflow.execute_activity(
            "generate_podcast_script_activity",
            args=[tenant_id, topic, research_results],
            start_to_close_timeout=timedelta(minutes=10)
        )
        
        # Step 3: Audio Synthesis
        audio_output = await workflow.execute_activity(
            "synthesize_audio_activity",
            args=[tenant_id, script_output],
            start_to_close_timeout=timedelta(minutes=15)
        )
        
        return {
            "status": "completed",
            "topic": topic,
            "script": script_output.get("script_raw"),
            "audio_url": audio_output.get("audio_url"),
            "duration": script_output.get("estimated_duration_mins")
        }

@workflow.defn
class VideoScriptWorkflow:
    @workflow.run
    async def run(self, tenant_id: str, topic: str) -> Dict[str, Any]:
        """
        Video Script Workflow:
        1. Generate script (scenes/visuals/audio).
        2. Create storyboard prompts.
        3. Generate SEO metadata.
        """
        # Step 1: Generate Script
        script_data = await workflow.execute_activity(
            "generate_video_script_activity",
            args=[tenant_id, topic],
            start_to_close_timeout=timedelta(minutes=10)
        )
        
        # Step 2: Storyboard
        storyboard = await workflow.execute_activity(
            "generate_storyboard_activity",
            args=[tenant_id, script_data.get("scenes", [])],
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        # Step 3: Metadata
        metadata = await workflow.execute_activity(
            "generate_video_metadata_activity",
            args=[tenant_id, topic],
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        return {
            "status": "completed",
            "topic": topic,
            "script": script_data,
            "storyboard": storyboard,
            "metadata": metadata
        }
