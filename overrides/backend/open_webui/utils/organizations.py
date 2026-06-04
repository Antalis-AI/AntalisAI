
import logging

from open_webui.models.groups import GroupForm, Groups

log = logging.getLogger(__name__)


async def apply_default_organization_assignment(
    default_organization_name: str,
    user_id: str,
    db=None,
) -> None:
    """
    Apply default organization assignment to a user if default_organization_name is provided.

    Args:
        default_organization_name: Name of the default organization to add the user to
        user_id: ID of the user to add to the default organization
    """
    if default_organization_name:
        try:
            try:
                # Assuming there's a method to get the organization ID by name
                organization_id = await Groups.get_group_by_name(default_organization_name, db=db)
            except AttributeError:
                try:  # If the organization doesn't exist, create it
                    group = await Groups.insert_new_group(
                        user_id,
                        GroupForm(
                            name=default_organization_name,
                            description='',
                            is_organization=True
                        ),
                        db=db
                    )
                    organization_id = group.id
                except Exception as e:
                    log.error(f'Failed to add user {user_id} to default organization {default_organization_name}: {e}')

            if organization_id:
                await Groups.add_users_to_group(organization_id, [user_id], db=db)
        except Exception as e:
            log.error(f'Failed to add user {user_id} to default organization {default_organization_name}: {e}')
