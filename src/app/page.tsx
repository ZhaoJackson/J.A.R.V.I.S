import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Welcome to J.A.R.V.I.S</h1>
          <p className="mt-2 text-sm text-gray-600">Your Personal Life Assistant</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Fitness Card */}
          <DashboardCard
            title="Fitness"
            description="Track your workouts and health metrics"
            icon="💪"
            href="/fitness"
          />

          {/* Social Media Card */}
          <DashboardCard
            title="Social Media"
            description="Manage your Instagram and social presence"
            icon="📱"
            href="/social"
          />

          {/* Calendar Card */}
          <DashboardCard
            title="Calendar"
            description="View and manage your schedule"
            icon="📅"
            href="/calendar"
          />

          {/* Books Card */}
          <DashboardCard
            title="Books"
            description="Track your reading list and progress"
            icon="📚"
            href="/books"
          />

          {/* Weather Card */}
          <DashboardCard
            title="Weather"
            description="Check current weather and forecasts"
            icon="🌤️"
            href="/weather"
          />

          {/* Finance Card */}
          <DashboardCard
            title="Finance"
            description="Monitor your personal finances"
            icon="💰"
            href="/finance"
          />

          {/* Learning Card */}
          <DashboardCard
            title="Learning"
            description="Track your Udemy courses and progress"
            icon="🎓"
            href="/learning"
          />

          {/* Projects Card */}
          <DashboardCard
            title="Projects"
            description="Monitor your GitHub repositories"
            icon="💻"
            href="/projects"
          />

          {/* Entertainment Card */}
          <DashboardCard
            title="Entertainment"
            description="Manage your music and YouTube content"
            icon="🎵"
            href="/entertainment"
          />
        </div>
      </main>
    </div>
  )
}

function DashboardCard({
  title,
  description,
  icon,
  href,
}: {
  title: string
  description: string
  icon: string
  href: string
}) {
  return (
    <Link
      href={href}
      className="block p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200"
    >
      <div className="flex items-center space-x-4">
        <span className="text-3xl">{icon}</span>
        <div>
          <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
          <p className="mt-1 text-sm text-gray-600">{description}</p>
        </div>
      </div>
    </Link>
  )
} 