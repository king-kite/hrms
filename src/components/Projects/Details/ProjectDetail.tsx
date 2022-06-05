import { FC } from "react";
import { FaUserPlus } from "react-icons/fa";
import { DEFAULT_IMAGE } from "../../../config";
import { useFormSelect } from "../../../hooks";
import { StatusProgressBar } from "../../common";
import { Button, Select } from "../../controls";
import { ProjectEmployeeType } from "../../../types"

export type ProjectDetailProps = {
	changePriority: (priority: string) => void;
	loading: boolean;
	priority: "L" | "M" | "H";
	leaders: ProjectEmployeeType[];
	team: ProjectEmployeeType[];
}

const ProjectDetail: FC<ProjectDetailProps> = ({ changePriority, loading, leaders, team, priority }) => {
	const level = useFormSelect(priority, {
		onChange: ({ value }) => changePriority(value)
	});

	return (
		<div className="py-2 w-full sm:px-4 lg:w-1/3">
			<div className="flex flex-col items-center md:flex-row md:items-start lg:flex-col lg:items-center">
				<div className="bg-white my-4 p-4 rounded-md shadow-lg w-full md:mr-6 md:w-[55%] lg:mr-0 lg:w-full">
					<h3 className="capitalize cursor-pointer font-bold text-lg text-gray-800 tracking-wide md:text-xl">
						project details
					</h3>
					<ul className="pb-1 pt-3">
						<li className="odd:bg-gray-100 rounded-sm flex items-center justify-between p-2 capitalize font-medium text-gray-800 text-base md:text-lg lg:text-base">
							<p>cost:</p>
							<p>$1200</p>
						</li>
						<li className="odd:bg-gray-100 rounded-sm flex items-center justify-between p-2 capitalize font-medium text-gray-800 text-base md:text-lg lg:text-base">
							<p>total hours:</p>
							<p>100 hours</p>
						</li>
						<li className="odd:bg-gray-100 rounded-sm flex items-center justify-between p-2 capitalize font-medium text-gray-800 text-base md:text-lg lg:text-base">
							<p>created:</p>
							<p>25 Feb, 2019</p>
						</li>
						<li className="odd:bg-gray-100 rounded-sm flex items-center justify-between p-2 capitalize font-medium text-gray-800 text-base md:text-lg lg:text-base">
							<p>deadline:</p>
							<p>12 Jun, 2019</p>
						</li>
						<li className="odd:bg-gray-100 rounded-sm flex items-center justify-between p-2 capitalize font-medium text-gray-800 text-base md:text-lg lg:text-base">
							<p>Priority:</p>
							<div>
								<Select
									bg={level.value === "H" ? "bg-red-100" : level.value === "M" ? "bg-yellow-100" : "bg-green-100"}
									bdrColor={level.value === "H" ? "border-red-600" : level.value === "M" ? "border-yellow-600" : "border-green-600"}
									color={level.value === "H" ? "text-red-700" : level.value === "M" ? "text-yellow-700" : "text-green-700"}
									disabled={loading}
									onChange={level.onChange}
									value={level.value}
									options={[
										{ title: "High", value: "H" },
										{ title: "Medium", value: "M" },
										{ title: "Low", value: "L" },
									]}
								/>
							</div>
						</li>
						<li className="odd:bg-gray-100 rounded-sm flex items-center justify-between p-2 capitalize font-medium text-gray-800 text-base md:text-lg lg:text-base">
							<p>created by</p>
							<p>barry cuda</p>
						</li>
						<li className="odd:bg-gray-100 rounded-sm flex items-center justify-between p-2 capitalize font-medium text-gray-800 text-base md:text-lg lg:text-base">
							<p>status:</p>
							<p>working</p>
						</li>
						<li className="rounded-sm flex items-center justify-between capitalize font-medium text-gray-800 text-base md:text-lg lg:text-base">
							<StatusProgressBar
								background="bg-green-600"
								containerColor="bg-white"
								border="border-none"
								title="Progress"
								result={0.4}
								value="40%"
							/>
						</li>
					</ul>
				</div>

				<div className="bg-white my-4 p-4 rounded-md shadow-lg w-full md:w-[45%] lg:w-full">
					<div className="flex items-center justify-between w-full">
						<h3 className="cursor-pointer font-bold text-lg text-gray-800 tracking-wide md:text-xl">
							Assigned Leader{leaders && leaders.length > 1 ? "s" : ""}
						</h3>
						<div>
							<Button 
								bold="normal"
								caps
								padding="px-2 py-1"
								title="add"
								IconRight={FaUserPlus}
							/>
						</div>
					</div>
					{leaders && leaders.length > 0 ? (
						<ul className="pb-1 pt-3">
							{leaders.map((leader, index) => (
								<li key={index} className="flex items-start rounded-md px-1 py-2 odd:bg-gray-100">
									<div className="w-[15%]">
										<div className="h-[30px] mx-1 w-[30px] rounded-full">
											<img className="h-full w-full" src={leader.image || DEFAULT_IMAGE} alt="" />
										</div>
									</div>
									<div className="px-2 w-[85%]">
										<p className="capitalize text-sm text-gray-800 md:text-base">
											{leader.full_name || "------"}
										</p>
										<span className="capitalize text-gray-600 text-xs md:text-sm">
											{leader.job || "-------"}
										</span>
									</div>
								</li>
							))}
						</ul>
					) : (
						<p className="text-sm text-gray-700">
							There are no assigned leaders
						</p>
					)}
				</div>
			</div>

			<div className="bg-white my-4 p-4 rounded-md shadow-lg w-full">
				<div className="flex items-center justify-between w-full">
					<h3 className="cursor-pointer font-bold text-lg text-gray-800 tracking-wide md:text-xl">
						Assigned Team
					</h3>
					<div>
						<Button 
							bold="normal"
							caps
							padding="px-2 py-1"
							title="add"
							IconRight={FaUserPlus}
						/>
					</div>
				</div>
				<ul className="grid grid-cols-1 pb-1 pt-3 sm:grid-cols-2 lg:grid-cols-1">
					{team && team.length > 0 ? (
						<ul className="pb-1 pt-3">
							{team.map((member, index) => (
								<li key={index} className="flex items-start rounded-md px-1 py-2 odd:bg-gray-100">
									<div className="w-[15%]">
										<div className="h-[30px] mx-1 w-[30px] rounded-full">
											<img className="h-full w-full" src={member.image || DEFAULT_IMAGE} alt="" />
										</div>
									</div>
									<div className="px-2 w-[85%]">
										<p className="capitalize text-sm text-gray-800 md:text-base">
											{member.full_name || "------"}
										</p>
										<span className="capitalize text-gray-600 text-xs md:text-sm">
											{member.job || "-------"}
										</span>
									</div>
								</li>
							))}
						</ul>
					) : (
						<p className="text-sm text-gray-700">
							There is no team
						</p>
					)}
				</ul>
			</div>
		</div>
	);
};

export default ProjectDetail;
