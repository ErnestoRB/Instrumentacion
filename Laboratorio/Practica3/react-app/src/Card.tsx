export interface ICardProps {
  title: string;
  children?: React.ReactNode;
}
export function Card({ title, children }: ICardProps) {
  return (
    <div className="flex flex-col border border-gray-200 p-4 rounded-lg shadow-sm gap-y-2">
      <h3 className="text-lg font-semibold">{title}</h3>
      <hr />
      {children}
    </div>
  );
}
