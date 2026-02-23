from __future__ import annotations

from discord_guild_configurator.models import (
    Category,
    ForumChannel,
    GuildConfig,
    PermissionOverwrite,
    Role,
    TextChannel,
    VoiceChannel,
)

COLOR_BLUE = "#0096C7"
COLOR_LIGHT_BLUE = "#8FD3E0"
COLOR_DARK_ORANGE = "#E6412C"
COLOR_ORANGE = "#E85D04"
COLOR_DARK_YELLOW = "#BC8C15"
COLOR_YELLOW = "#FFD700"
COLOR_PURPLE = "#D34EA5"
COLOR_GREY = "#99AAB5"
COLOR_DARK_PURPLE = "#658B34"
ROLE_COC = "Code of Conduct Committee"
ROLE_MODERATORS = "Moderators"
ROLE_ORGANIZERS = "Organizers"
ROLE_VOLUNTEERS = "Volunteers"
ROLE_SPEAKERS = "Speakers"
ROLE_SPONSORS = "Sponsors"
ROLE_PARTICIPANTS = "Participants"
ROLE_EVERYONE = "@everyone"
ROLE_BEGINNERS_DAY = "Beginners Day"
ROLES_COC = [ROLE_COC]
ROLES_MODERATORS = [ROLE_MODERATORS, *ROLES_COC]
ROLES_ORGANIZERS = [ROLE_ORGANIZERS, *ROLES_MODERATORS]
ROLES_VOLUNTEERS = [ROLE_VOLUNTEERS, *ROLES_ORGANIZERS]
ROLES_SPEAKERS = [ROLE_SPEAKERS, *ROLES_ORGANIZERS]
ROLES_SPONSORS = [ROLE_SPONSORS, *ROLES_ORGANIZERS]
ROLES_REGISTERED = [
    ROLE_PARTICIPANTS,
    ROLE_SPONSORS,
    ROLE_SPEAKERS,
    *ROLES_VOLUNTEERS,
    ROLE_BEGINNERS_DAY,
]
CONFIG = GuildConfig(
    roles=[
        Role(
            name=ROLE_COC,
            color=COLOR_DARK_ORANGE,
            hoist=True,
            mentionable=True,
            permissions=[
                "kick_members",
                "ban_members",
                "priority_speaker",
                "deafen_members",
                "mute_members",
            ],
        ),
        Role(
            name=ROLE_MODERATORS,
            color=COLOR_ORANGE,
            hoist=True,
            mentionable=True,
            permissions=[
                "manage_nicknames",
                "moderate_members",
                "manage_messages",
                "manage_threads",
                "priority_speaker",
                "deafen_members",
                "mute_members",
            ],
        ),
        Role(
            name=ROLE_ORGANIZERS,
            color=COLOR_DARK_YELLOW,
            permissions=["mention_everyone", "use_external_apps", "manage_roles"],
        ),
        Role(
            name=ROLE_VOLUNTEERS,
            color=COLOR_YELLOW,
            hoist=True,
            mentionable=True,
        ),
        Role(name="Onsite Volunteers", color=COLOR_GREY),
        Role(name="Remote Volunteers", color=COLOR_GREY),
        Role(
            name=ROLE_SPEAKERS,
            color=COLOR_BLUE,
            hoist=True,
            mentionable=True,
        ),
        Role(
            name=ROLE_SPONSORS,
            color=COLOR_LIGHT_BLUE,
            hoist=True,
            mentionable=True,
        ),
        Role(
            name=ROLE_PARTICIPANTS,
            color=COLOR_PURPLE,
            hoist=True,
            mentionable=True,
            permissions=["use_external_emojis", "use_external_stickers", "create_polls"],
        ),
        Role(name="Onsite Participants", color=COLOR_GREY),
        Role(name="Remote Participants", color=COLOR_GREY),
        Role(
            name=ROLE_BEGINNERS_DAY,
            color=COLOR_DARK_PURPLE,
            mentionable=True,
            permissions=["use_external_emojis", "use_external_stickers", "create_polls"],
        ),
        Role(name="Programme Team", color=COLOR_GREY, mentionable=True),
        Role(
            name="@everyone",
            color=COLOR_GREY,
            permissions=[
                "view_channel",
                "change_nickname",
                "send_messages",
                "send_messages_in_threads",
                "create_public_threads",
                "embed_links",
                "attach_files",
                "add_reactions",
                "read_message_history",
                "use_application_commands",
                "connect",
                "speak",
                "use_voice_activation",
            ],
        ),
    ],
    rules_channel_name="rules",
    system_channel_name="system-events",
    updates_channel_name="discord-updates",
    categories=[
        Category(
            name="Information",
            channels=[
                TextChannel(
                    name="rules",
                    topic="Please read the rules carefully!",
                    channel_messages=[
                        """
                        ## Community Rules

                        **Rule 1**
                        Follow the [EuroPython Society Code of Conduct](https://www.europython-society.org/coc/).
                        **Rule 2**
                        Use English to the best of your ability. Be polite if someone speaks English imperfectly.
                        **Rule 3**
                        Use the name on your ticket as your display name. This will be done automatically during the #registration-form process.
                        **Rule 4**
                        When posting pictures, please keep visually impaired attendees in mind. A short description can make a big difference.
                        See also: [Discord - Add Alt Text To Your Image Upload](https://support.discord.com/hc/en-us/articles/211866427-How-do-I-upload-images-and-GIFs#h_01GWWTHYJEV2S1WCDGFEMY21AQ)

                        **Reporting Incidents**
                        If you notice something that needs the attention of a moderator of the community, please ping the <<@&Moderators>> role.

                        Note that not all moderators are a member of the EuroPython Code of Conduct team. See the <<#code-of-conduct>> channel to read how you can report Code of Conduct incidents.
                        """  # noqa: E501 (line too long)
                    ],
                ),
                TextChannel(
                    name="code-of-conduct",
                    topic="https://www.europython-society.org/coc/",
                    channel_messages=[
                        """
                        ## EuroPython Society Code of Conduct
                        EuroPython is a community conference intended for networking and collaboration in the developer community.

                        We value the participation of each member of the Python community and want all participants to have an enjoyable and fulfilling experience. Accordingly, all attendees are expected to show respect and courtesy to other attendees throughout the conference and at all conference events.

                        To make clear what is expected, all staff, attendees, speakers, exhibitors, organisers, and volunteers at any EuroPython event are required to conform to the [Code of Conduct](https://www.europython-society.org/coc/), as set forth by the [EuroPython Society](https://www.europython-society.org/about/). Organisers will enforce this code throughout the event.

                        **Please read the Code of Conduct:** https://www.europython-society.org/coc/
                        """,  # noqa: E501 (line too long)
                        """
                        ## Reporting Incidents
                        **If you believe someone is in physical danger, including from themselves**, the most important thing is to get that person help. Please contact the appropriate crisis number, non-emergency number, or police number. If you are a EuroPython attendee, you can consult with a volunteer or organiser to help find an appropriate number.

                        If you believe a [Code of Conduct](https://www.europython-society.org/coc/) incident has occurred, we encourage you to report it. If you are unsure whether the incident is a violation, or whether the space where it happened is covered by the Code of Conduct, we encourage you to still report it. We are fine with receiving reports where we decide to take no action for the sake of creating a safer space.
                        """,  # noqa: E501 (line too long)
                        """
                        ## General Reporting Procedure
                        If you are being harassed, notice that someone else is being harassed, or have any other concerns, please contact a member of the Code of Conduct committee immediately:
                        - Email: [coc@europython.eu](mailto:coc@europython.eu)
                        - Discord role: <<@&Code of Conduct Committee>>
                        - Individual contact information: [EPS Website](https://www.europython-society.org/coc/#contact-information)
                        """,  # noqa: E501 (line too long)
                        """
                        ## Links
                        - [EuroPython Society Code of Conduct](https://www.europython-society.org/coc/)
                        - [Incident Reporting Procedure](https://www.europython-society.org/coc-incident-reporting/)
                        - [Procedure for Incident Response](https://www.europython-society.org/coc-enforcement-procedure/)
                        """,
                    ],
                ),
                ForumChannel(
                    name="job-board",
                    topic="""
                        Make sure your job openings follows the following rules:

                        1. Title: A clear and concise title including the role and the Company/Organization
                        2. Job Type: Indicate whether the job is full-time, part-time, contract-based, freelance, or an internship.
                        3. Job Description: Provide a URL or text explaining the job.
                        4. Application Deadline: If there is a specific deadline for applications, mention it in the post.
                        5. Salary/Compensation: If possible and appropriate, include salary or compensation details.
                        6. Additional Information: stuff like:  perks, or notable company culture, include them in the post.
                        7. Relevant Tags: Use relevant tags or keywords to categorize the job post. Please let us know if important tags are missing.
                        8. No Discrimination: Ensure that the job post does not include any discriminatory language or requirements.
                        9. Updates and Removal: If the job position is filled or no longer available, update or remove the post to avoid confusion for job seekers.
                        """,  # noqa: E501 (line too long)
                    tags=[
                        "Remote",
                        "Hybrid",
                        "On-site",
                        "AI",
                        "Data Science",
                        "Data Engineering",
                        "Backend",
                        "Frontend",
                        "Full Stack",
                        "Cloud",
                        "Web",
                        "DevOps",
                        "Junior",
                        "Professional",
                        "Senior",
                    ],
                    require_tag=True,
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=ROLES_SPONSORS, allow=["send_messages", "create_public_threads"]
                        ),
                    ],
                ),
            ],
            permission_overwrites=[
                PermissionOverwrite(
                    roles=[ROLE_EVERYONE],
                    deny=["send_messages", "create_public_threads", "add_reactions"],
                )
            ],
        ),
        Category(
            name="EuroPython 2025",
            channels=[
                TextChannel(
                    name="announcements",
                    topic="Organisers will make EuroPython announcements in this channel",
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=[ROLE_EVERYONE], deny=["send_messages", "create_public_threads"]
                        ),
                        PermissionOverwrite(roles=[ROLE_ORGANIZERS], allow=["send_messages"]),
                    ],
                ),
                TextChannel(
                    name="general-chat",
                    topic=(
                        "Social chat for conference participants. "
                        "Please follow the Rules and Code of Conduct."
                    ),
                ),
                ForumChannel(
                    name="support",
                    topic="""
                        Use this forum channel to create support tickets if you **need support from the conference organization**. Please don't open forum threads related to other topics, as that makes it difficult for the organizers to keep track of support tickets that need their attention.

                        If you to make a report to the Code of Conduct Committee, please use coc@europython.eu or contact an organizer at the conference.
                        """,  # noqa: E501 (line too long)
                    tags=["Remote Support", "On-Site Support"],
                    require_tag=True,
                ),
                ForumChannel(
                    name="feedback",
                    topic="""
                    Please share your thoughts and ideas. What works well? What doesn't? How can we make EuroPython even better?
                    """,  # noqa: E501 (line too long)
                ),
                TextChannel(
                    name="introduction",
                    topic="Feel free to introduce yourself here :)",
                ),
                TextChannel(
                    name="ask-the-locals",
                    topic="""
                    The right place to ask locals for help and experience.
                    Many people recommended the YouTube channel 'HONEST GUIDE', maybe you find it helpful as well: https://www.youtube.com/@HONESTGUIDE
                    """,  # noqa: E501 (line too long)
                ),
                ForumChannel(
                    name="topics-and-interests",
                    topic="""
                        You can use this forum channel to start conversations focused around specific topics and interests, including topics unrelated to EuroPython or Python. Think of it like a virtual hallway track where you can discuss topics with the people you meet while participating in a conference.

                        **Use a descriptive title** that clearly highlights the topic you intend to discuss within this channel. However, do **keep in mind that conversations tend to meander away from their initial topic over time**. While it's okay to nudge the conversation back onto its original topic, do **be patient and civil** with each other, even if you perceive someone as going "off-topic".

                        Thank you for your cooperation in maintaining an open and welcoming environment for everyone!
                        """,  # noqa: E501 (line too long)
                ),
                ForumChannel(
                    name="social-activities",
                    topic="""
                        # Social Activities organized by and for attendees
                        You can use this channel to organize a social activity with other attendees of the conference. Do note that EuroPython only provides a space for attendees to coordinate social activities, it does not officially endorse activities posted here.

                        ## topic for a good post
                        - Use a **descriptive title** that captures the core of your activity
                        - If relevant, **include the date and time in your title**
                        - Indicate if your activity is **in-person** or **remote** by selecting the appropriate tag
                        """,  # noqa: E501 (line too long)
                    tags=["In Person", "Remote"],
                    require_tag=True,
                ),
                TextChannel(
                    name="lost-and-found",
                    topic=(
                        "Channel for the coordination of lost and found items. "
                        "Please bring found items to the registration desk."
                    ),
                ),
            ],
            permission_overwrites=[
                PermissionOverwrite(roles=[ROLE_EVERYONE], deny=["view_channel"]),
                PermissionOverwrite(roles=ROLES_REGISTERED, allow=["view_channel"]),
            ],
        ),
        Category(
            name="Remote Attendees",
            channels=[
                TextChannel(name="remote-text", topic="Text chat for remote attendees"),
                VoiceChannel(name="remote-voice"),
            ],
            permission_overwrites=[
                PermissionOverwrite(roles=[ROLE_EVERYONE], deny=["view_channel"]),
                PermissionOverwrite(roles=ROLES_REGISTERED, allow=["view_channel"]),
            ],
        ),
        Category(
            name="Sponsors",
            channels=[],
            permission_overwrites=[
                PermissionOverwrite(roles=[ROLE_EVERYONE], deny=["view_channel"]),
                PermissionOverwrite(roles=ROLES_REGISTERED, allow=["view_channel"]),
            ],
        ),
        Category(
            name="Rooms",
            channels=[
                TextChannel(
                    name="programme-notifications",
                    topic="Find the latest information about starting sessions here!",
                    permission_overwrites=[
                        PermissionOverwrite(roles=[ROLE_EVERYONE], deny=["send_messages"])
                    ],
                ),
                TextChannel(name="forum-hall", topic="Livestream: [TBA]"),
                TextChannel(name="south-hall-2a", topic="Livestream: [TBA]"),
                TextChannel(name="south-hall-2b", topic="Livestream: [TBA]"),
                TextChannel(name="north-hall", topic="Livestream: [TBA]"),
                TextChannel(name="terrace-2a", topic="Livestream: [TBA]"),
                TextChannel(name="terrace-2b", topic="Livestream: [TBA]"),
                TextChannel(
                    name="exhibit-hall", topic="For conversations related to the exhibit hall."
                ),
                TextChannel(
                    name="open-spaces",
                    topic=(
                        "For conversations related to the open spaces. Schedule and booking: [TBA]"
                    ),
                ),
                ForumChannel(
                    name="tutorials",
                    topic="""
                        We kindly ask you to **only create one thread per tutorial**. Having too many threads makes it more difficult for participants to find the thread of the tutorial they're participating in.

                        **Tips:**
                        - On desktop, you can open a forum thread in "full window mode" using the `...` option menu in the top bar.
                        - If you select to "follow" a thread, it will appear directly in your channel list.
                        """,  # noqa: E501 (line too long)
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=ROLES_REGISTERED,
                            deny=["create_public_threads"],
                        ),
                        PermissionOverwrite(
                            roles=ROLES_SPEAKERS,
                            allow=["create_public_threads"],
                        ),
                    ],
                ),
                ForumChannel(
                    name="sprints",
                    topic=(
                        "To keep things manageable, one post/thread per sprint would be the best."
                        "If there are reasons to create multiple threads/posts "
                        "(e.g., for groups working on a sub-project), that should be fine, too."
                    ),
                ),
                ForumChannel(
                    name="beginners-day",
                    topic=(
                        "Channel for the Beginners' Day: "
                        "https://ep2025.europython.eu/beginners-day/"
                    ),
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=[ROLE_BEGINNERS_DAY],
                            allow=["view_channel"],
                        ),
                    ],
                ),
                ForumChannel(
                    name="slides-and-artefacts",
                    topic="""
                        You can create a thread for your talk where you can add slides and other artefacts.

                        - Please add the **title of your talk **and the **names of the speakers** in the title. This makes it easy for participants to find your talk.
                        - Only create a single post per talk!
                        - Participants can't send messages in the thread.
                        """,  # noqa: E501 (line too long)
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=ROLES_REGISTERED,
                            deny=["create_public_threads"],
                        ),
                        PermissionOverwrite(
                            roles=ROLES_SPEAKERS,
                            allow=["create_public_threads"],
                        ),
                    ],
                ),
            ],
            permission_overwrites=[
                PermissionOverwrite(roles=[ROLE_EVERYONE], deny=["view_channel"]),
                PermissionOverwrite(roles=ROLES_REGISTERED, allow=["view_channel"]),
            ],
        ),
        Category(
            name="Conference Organization",
            channels=[
                TextChannel(
                    name="announcements-volunteers",
                    topic=(
                        "Announcements and requests for conference volunteers. "
                        "Please use <<#volunteers-lounge>> for all other "
                        "volunteer-related conversations."
                    ),
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=ROLES_VOLUNTEERS,
                            allow=["view_channel"],
                        ),
                    ],
                ),
                TextChannel(
                    name="volunteers-lounge",
                    topic=(
                        "Social chat for volunteers. Please follow the #rules and #code-of-conduct!"
                    ),
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=ROLES_VOLUNTEERS,
                            allow=["view_channel"],
                        ),
                    ],
                ),
                TextChannel(
                    name="sponsors-lounge",
                    topic=(
                        "Social chat for sponsors. Please follow the #rules and #code-of-conduct!"
                    ),
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=[*ROLES_SPONSORS, *ROLES_VOLUNTEERS],
                            allow=["view_channel"],
                        ),
                    ],
                ),
                TextChannel(
                    name="speakers-lounge",
                    topic=(
                        "Channel open to all speakers & conference volunteers. "
                        "Please follow the #rules and #code-of-conduct!"
                    ),
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=[*ROLES_SPEAKERS, *ROLES_VOLUNTEERS],
                            allow=["view_channel"],
                        ),
                    ],
                ),
                TextChannel(
                    name="moderators",
                    topic=(
                        "For discussions related to ongoing moderation activities, "
                        "moderation policy, and other moderation-related topic."
                    ),
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=ROLES_MODERATORS,
                            allow=["view_channel"],
                        ),
                    ],
                ),
                TextChannel(
                    name="discord-updates",
                    topic="Discord will send community server notifications here.",
                ),
            ],
            permission_overwrites=[
                PermissionOverwrite(roles=[ROLE_EVERYONE], deny=["view_channel"]),
            ],
        ),
        Category(
            name="Registration",
            channels=[
                TextChannel(
                    name="welcome",
                    topic="Welcome to our server, please register.",
                    channel_messages=[
                        """
                        **Welcome to our Discord server! Please register using the <<#registration-form>>**

                        If you encounter any problems with registration, please ask in <<#registration-help>>.
                        """,  # noqa: E501 (line too long)
                    ],
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=[ROLE_EVERYONE], deny=["send_messages", "create_public_threads"]
                        ),
                        PermissionOverwrite(roles=ROLES_REGISTERED, deny=["view_channel"]),
                        PermissionOverwrite(roles=ROLES_ORGANIZERS, allow=["view_channel"]),
                    ],
                ),
                TextChannel(
                    name="registration-form",
                    topic="Please follow the registration instructions.",
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=[ROLE_EVERYONE], deny=["send_messages", "create_public_threads"]
                        ),
                        PermissionOverwrite(roles=ROLES_REGISTERED, deny=["view_channel"]),
                        PermissionOverwrite(roles=ROLES_ORGANIZERS, allow=["view_channel"]),
                    ],
                ),
                ForumChannel(
                    name="registration-help",
                    topic="""
                        # This channel is only for asking for help with registration, not for general discussion.

                        As this community is only intended for EuroPython participants, there are no public discussion channels.
                        """,  # noqa: E501 (line too long)
                    permission_overwrites=[
                        PermissionOverwrite(roles=ROLES_REGISTERED, deny=["view_channel"]),
                        PermissionOverwrite(roles=ROLES_ORGANIZERS, allow=["view_channel"]),
                    ],
                ),
                TextChannel(
                    name="registration-log",
                    topic=(
                        "The EuroPython bot will log registration actions here "
                        "to help us with debugging."
                    ),
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=[ROLE_EVERYONE],
                            deny=["view_channel"],
                        )
                    ],
                ),
                TextChannel(
                    name="system-events",
                    topic=(
                        'This channel will show "raw" joins to keep track of who joins '
                        "and who registered without diving into the audit log."
                    ),
                    permission_overwrites=[
                        PermissionOverwrite(
                            roles=[ROLE_EVERYONE],
                            deny=["view_channel"],
                        )
                    ],
                ),
            ],
        ),
    ],
)
