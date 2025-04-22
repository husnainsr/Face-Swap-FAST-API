from apscheduler.schedulers.background import BackgroundScheduler
from app.services.image_service import ImageService

def setup_image_cleanup_scheduler():
    """
    Schedules periodic cleanup of expired images.
    
    Returns:
        BackgroundScheduler: The configured scheduler instance
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        ImageService.cleanup_old_images,
        'interval',
        hours=1,  # Run every hour
        id='cleanup_images'
    )
    scheduler.start()
    return scheduler 