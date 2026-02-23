export type OverviewResponse = {
  current: Record<string, number>
  previous: Record<string, number>
  comments: string[]
}

export type ChannelRow = {
  channel: string
  visits: number
  orders: number
  revenue: number
  cost: number
  conversion: number
  romi: number
}
