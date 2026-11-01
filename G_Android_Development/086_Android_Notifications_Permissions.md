================================================================================
  FILE 086: ANDROID NOTIFICATIONS, PERMISSIONS, & INTENTS
  Section: G - Android Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Android Notifications & Runtime Permissions
  Modern Android OS heavily restricts background actions, hardware access, and user interruptions to protect privacy and prevent spam. This guide covers how to correctly request runtime permissions, build rich notifications, manage notification channels, and handle inter-process communication using Intents and PendingIntents.
  Prerequisites: Android Context, Activity lifecycles, and BroadcastReceivers.
  What you'll learn: Notification Channels, NotificationCompat.Builder, FCM Push Notifications, the modern ActivityResultContracts permission request flow, and intent flags.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  NOTIFICATION CHANNEL
    Required on Android 8.0+. A grouping of notifications that allows the user to disable or change the sound/vibration for a specific type of notification rather than the whole app.

  NOTIFICATIONCOMPAT.BUILDER
    The backward-compatible builder class used to construct the UI of a notification (icons, text, styles, action buttons).

  PENDINGINTENT
    A token that you give to a foreign application (like the Android Notification Manager or AlarmManager), which allows the foreign application to use your app's permissions to execute a predefined piece of code.

  FLAG_IMMUTABLE
    A critical security flag for PendingIntents introduced recently, preventing malicious apps from altering the intent data before it fires.

  PUSH NOTIFICATIONS (FCM)
    Firebase Cloud Messaging. Consists of Notification Messages (handled automatically by the system UI) and Data Messages (delivered to the app silently via FirebaseMessagingService).

  RUNTIME PERMISSIONS
    Required on Android 6.0+. Dangerous permissions (Camera, Location, Contacts) must be requested from the user dynamically while the app is running, not just at install time.

  POST_NOTIFICATIONS
    A specific runtime permission introduced in Android 13 (API 33) required to show any local or push notifications.

  ACTIVITYRESULTCONTRACTS
    The modern, lifecycle-aware way to request permissions or start an Activity for a result, replacing the deprecated startActivityForResult.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  RUNTIME PERMISSION FLOW                                                │
  │                                                                         │
  │         [ Request Action (e.g., Open Camera) ]                          │
  │                          |                                              │
  │          Is permission already granted?                                 │
  │            /                      \                                     │
  │        [Yes]                      [No]                                  │
  │          |                          |                                   │
  │     (Open Camera)        Should show rationale? (Did user deny previously?)│
  │                             /                \                          │
  │                          [Yes]               [No]                       │
  │                            |                   |                        │
  │                  (Show Custom Dialog)  (System Permission Dialog)       │
  │                  Explaining *why* ->       |                            │
  │                  we need it.            User Action                     │
  │                                         /         \                     │
  │                                    [Deny]      [Grant]                  │
  │                                      |            |                     │
  │                                (Show Error)   (Open Camera)             │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  PUSH NOTIFICATION DELIVERY (FCM)                                       │
  │                                                                         │
  │   +---------------+       +--------------+       +------------------+   │
  │   | Backend Server| ----> | FCM Server   | ----> | Android OS       |   │
  │   +---------------+       +--------------+       +------------------+   │
  │                                                          |              │
  │                                         +----------------+----------------+│
  │                                         |                                 |│
  │                                 [App in Background]               [App in Foreground]│
  │                                         |                                 |│
  │                                OS shows Notification             Delivered to App via│
  │                                automatically.                    FirebaseMessagingService.│
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Requesting Permissions (Modern Approach)                             │
  │                                                                          │
  │  class CameraActivity : AppCompatActivity() {                            │
  │                                                                          │
  │      // 1. Register the Permission Launcher using the modern Activity Result API│
  │      private val requestCameraPermissionLauncher = registerForActivityResult(│
  │          ActivityResultContracts.RequestPermission()                     │
  │      ) { isGranted: Boolean ->                                           │
  │          if (isGranted) {                                                │
  │              openCamera()                                                │
  │          } else {                                                        │
  │              Toast.makeText(this, "Camera permission denied", Toast.LENGTH_SHORT).show()│
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      fun onCameraButtonClicked() {                                       │
  │          when {                                                          │
  │              ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)│
  │                  == PackageManager.PERMISSION_GRANTED -> {               │
  │                  // Permission already granted                           │
  │                  openCamera()                                            │
  │              }                                                           │
  │              ActivityCompat.shouldShowRequestPermissionRationale(this, Manifest.permission.CAMERA) -> {│
  │                  // User previously denied, show explanation before asking again│
  │                  showRationaleDialog {                                   │
  │                      requestCameraPermissionLauncher.launch(Manifest.permission.CAMERA)│
  │                  }                                                       │
  │              }                                                           │
  │              else -> {                                                   │
  │                  // First time asking                                    │
  │                  requestCameraPermissionLauncher.launch(Manifest.permission.CAMERA)│
  │              }                                                           │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      private fun openCamera() { /* Launch CameraX or Intent */ }         │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  [Language: kotlin]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  class NotificationHelper(private val context: Context) {                │
  │                                                                          │
  │      companion object {                                                  │
  │          const val CHANNEL_ID = "message_alerts"                         │
  │          const val NOTIFICATION_ID = 101                                 │
  │      }                                                                   │
  │                                                                          │
  │      fun createNotificationChannel() {                                   │
  │          // Channels are required on API 26+                             │
  │          if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {           │
  │              val name = "Message Alerts"                                 │
  │              val descriptionText = "Notifications for incoming chat messages"│
  │              val importance = NotificationManager.IMPORTANCE_HIGH        │
  │                                                                          │
  │              val channel = NotificationChannel(CHANNEL_ID, name, importance).apply {│
  │                  description = descriptionText                           │
  │                  enableVibration(true)                                   │
  │                  enableLights(true)                                      │
  │                  lightColor = Color.RED                                  │
  │              }                                                           │
  │                                                                          │
  │              val notificationManager: NotificationManager =              │
  │                  context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager│
  │              notificationManager.createNotificationChannel(channel)      │
  │          }                                                               │
  │      }                                                                   │
  │                                                                          │
  │      fun showMessageNotification(senderName: String, messageText: String) {│
  │          // 1. Create an Intent that opens the App when notification is tapped│
  │          val intent = Intent(context, ChatActivity::class.java).apply {  │
  │              flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK│
  │          }                                                               │
  │                                                                          │
  │          // 2. Wrap it in a PendingIntent. FLAG_IMMUTABLE is required for security on Android 12+│
  │          val pendingIntent: PendingIntent = PendingIntent.getActivity(   │
  │              context, 0, intent, PendingIntent.FLAG_IMMUTABLE            │
  │          )                                                               │
  │                                                                          │
  │          // 3. Build the Notification                                    │
  │          val builder = NotificationCompat.Builder(context, CHANNEL_ID)   │
  │              .setSmallIcon(R.drawable.ic_message) // Small icon is MANDATORY│
  │              .setContentTitle("New message from $senderName")            │
  │              .setContentText(messageText)                                │
  │              .setPriority(NotificationCompat.PRIORITY_HIGH) // For backward compatibility < API 26│
  │              .setContentIntent(pendingIntent) // Tap action              │
  │              .setAutoCancel(true) // Removes notification when tapped    │
  │              .setStyle(NotificationCompat.BigTextStyle().bigText(messageText)) // Expandable text│
  │                                                                          │
  │          // 4. Check for Android 13+ Notification Permission             │
  │          if (ActivityCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {│
  │              // Need to request POST_NOTIFICATIONS permission from the Activity│
  │              return                                                      │
  │          }                                                               │
  │                                                                          │
  │          // 5. Fire it                                                   │
  │          NotificationManagerCompat.from(context).notify(NOTIFICATION_ID, builder.build())│
  │      }                                                                   │
  │  }                                                                       │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is a Notification Channel and why was it introduced?

  ANSWER:
    Introduced in Android 8 (API 26), Channels group notifications by category (e.g., "Marketing", "Direct Messages"). It allows the user to disable annoying promotional notifications while keeping critical message notifications enabled, preventing them from disabling all app notifications.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What is the difference between a Notification Message and a Data Message in FCM?

  ANSWER:
    - Notification Message: Handled automatically by the system tray if the app is in the background. The app's code is not executed until the user taps it.
    - Data Message: Delivered silently to FirebaseMessagingService.onMessageReceived(). The app is woken up, can process the JSON payload, and manually trigger a local notification or update the database.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: What is a PendingIntent and why is FLAG_IMMUTABLE important?

  ANSWER:
    A PendingIntent wraps an intent, granting a foreign app (like the System Notification Manager) the right to execute that intent using your app's identity. FLAG_IMMUTABLE ensures the foreign app cannot alter the internal intent data (e.g., redirecting the intent to a malicious component) before firing it.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: Explain the purpose of shouldShowRequestPermissionRationale().

  ANSWER:
    It returns true if the user previously denied the permission request. It signals the developer that they should display a custom UI dialogue explaining why the app needs the permission before triggering the system prompt again.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How did permission requesting change in Android 13 (API 33) regarding notifications?

  ANSWER:
    Prior to API 33, apps could show notifications by default. In Android 13+, apps must explicitly ask for the POST_NOTIFICATIONS runtime permission.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Why is startActivityForResult deprecated, and what replaced it?

  ANSWER:
    It tightly coupled the request and result handling inside the Activity via onActivityResult overriding, leading to massive, unreadable when/switch blocks. It was replaced by ActivityResultContracts, which are lifecycle-aware, type-safe, and cleanly separate different intents via distinct launchers.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the SmallIcon requirement in NotificationCompat?

  ANSWER:
    A setSmallIcon() is mandatory. If you attempt to build and notify a NotificationCompat object without a small icon, the app will instantly crash with an IllegalArgumentException.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: If the user explicitly denies a permission multiple times, what happens?

  ANSWER:
    The OS will auto-deny future requests. The system dialog won't even appear. The developer must detect this and guide the user to the OS Settings app using an intent (ACTION_APPLICATION_DETAILS_SETTINGS) to toggle it manually.

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Crashy Notification

  val builder = NotificationCompat.Builder(context, "my_channel")
      .setContentTitle("Hello")
      .setContentText("World!")
      
  NotificationManagerCompat.from(context).notify(1, builder.build())

  SOLUTION:
    Problem: It will crash. setSmallIcon() is missing. It is the only strictly required UI element for an Android notification.
    Fix: Add .setSmallIcon(R.drawable.ic_notification).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Silent App in Background

  // FCM Payload sent from server:
  {
    "to": "device_token",
    "notification": {
      "title": "Sync Data",
      "body": "Download latest configs"
    },
    "data": {
      "config_id": "123"
    }
  }

  SOLUTION:
    Problem: The developer expects onMessageReceived() to run in the background to sync the config. However, because the payload contains a "notification" block, the Android OS intercepts it when the app is in the background, displays a system notification, and DOES NOT call onMessageReceived().
    Fix: If you want reliable background execution for sync purposes, send a pure "Data Message" (omit the "notification" key completely).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Security Exception on Android 12

  val pendingIntent = PendingIntent.getActivity(context, 0, intent, 0)

  SOLUTION:
    Problem: Running this on Android 12+ (API 31+) will throw an IllegalArgumentException. The system strictly requires specifying mutability flags.
    Fix: Use PendingIntent.FLAG_IMMUTABLE (or FLAG_MUTABLE if explicitly necessary) as the last argument.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Mismanaging permissions leads directly to app uninstalls. If an app requests Camera permission on launch without explanation, users reject it. Furthermore, failing to handle FCM payloads correctly (Data vs Notification) causes massive discrepancies in production—users will get notifications but the app state won't update, or silent data syncs will fail to trigger.

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 083: Background Processing (Foreground Services) (relationship description)
  -> File 085: Offline-First Sync (FCM Triggering sync) (relationship description)

================================================================================
  END OF FILE 086
================================================================================
